import time

from langsmith import traceable
from langchain_ollama import ChatOllama
from src.tools.tools import (
    web_search,
    scrape_url
)

from src.graph.state import ResearchState

from src.prompts.writer_prompt import (
    writer_prompt
)

from src.prompts.critic_prompt import (
    critic_prompt
)

from src.observability.metrics import (
    track_metrics
)

from src.observability.logging_config import (
    logger
)


from dotenv import load_dotenv
import os

load_dotenv()

mode = os.getenv("OLLAMA_MODEL")
base_url = os.getenv("OLLAMA_BASE_URL")


llm = ChatOllama(
    model="llama3.2:3b",
    base_url=base_url,
    temperature=0
)



# SEARCH NODE

@traceable(name="search_node")
def search_node(state: ResearchState):

    start = time.time()

    logger.info("SEARCH NODE STARTED")

    result = web_search.invoke(
        state["topic"]
    )

    state["search_results"] = str(result)

    urls = []

    if result["status"] == "success":

        for item in result["data"]:
            urls.append(item["url"])

    state["sources"] = urls

    state["metrics"]["search"] = track_metrics(
        "search_node",
        start
    )

    return state


# READER NODE

@traceable(name="reader_node")
def reader_node(state: ResearchState):

    start = time.time()

    logger.info("READER NODE STARTED")

    contents = []

    for url in state["sources"][:3]:

        result = scrape_url.invoke(url)

        if result["status"] == "success":

            contents.append(result["content"])

    state["scraped_content"] = "\n\n".join(
        contents
    )

    state["metrics"]["reader"] = track_metrics(
        "reader_node",
        start
    )

    return state


# WRITER NODE

@traceable(name="writer_node")
def writer_node(state: ResearchState):

    start = time.time()

    logger.info("WRITER NODE STARTED")

    chain = writer_prompt | llm

    response = chain.invoke({

        "topic": state["topic"],

        "research": (
            state["search_results"]
            + "\n\n" +
            state["scraped_content"]
        )
    })

    state["report"] = response.content

    state["metrics"]["writer"] = track_metrics(
        "writer_node",
        start
    )

    return state


# CRITIC NODE

@traceable(name="critic_node")
def critic_node(state: ResearchState):

    start = time.time()

    logger.info("CRITIC NODE STARTED")

    try:

        chain = critic_prompt | llm

        # DEBUG REPORT LENGTH
        print("Report Length:", len(state.get("report", "")))

        # LIMIT INPUT SIZE
        short_report = state.get("report", "")[:4000]

        response = chain.invoke({
            "report": short_report
        })

        state["evaluation"] = response.content

        state["critique"] = response.content

    except Exception as e:

        logger.error(f"Critic Node Error: {e}")

        state["evaluation"] = "Failed to evaluate report."

        state["critique"] = "Failed to evaluate report."

    state["metrics"]["critic"] = track_metrics(
        "critic_node",
        start
    )

    return state