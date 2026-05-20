import streamlit as st
import time
import pandas as pd

from src.graph.workflow import graph


# PAGE CONFIG

st.set_page_config(
    page_title="ResearchAgent",
    page_icon="🔬",
    layout="wide"
)

# SESSION STATE

if "results" not in st.session_state:
    st.session_state.results = None

# HEADER

st.title("🔬 Multi-Agent Research System")

st.markdown("""
AI-powered research pipeline using:

- LangGraph
- LangSmith Observability
- Multi-Agent Architecture
- Streamlit Dashboard
""")

# INPUT

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Future of AI Agents"
)

run_button = st.button(
    "Run Research Pipeline"
)

# RUN GRAPH

if run_button:

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        with st.spinner(
            "Running Multi-Agent Pipeline..."
        ):

            start = time.time()

            result = graph.invoke({

                "topic": topic,

                "search_results": "",

                "scraped_content": "",

                "report": "",

                "critique": "",

                "sources": [],

                "metrics": {},

                # FIXED
                "evaluation": ""
            })

            total_time = (
                time.time() - start
            )

            result["total_runtime"] = round(
                total_time,
                2
            )

            st.session_state.results = result

# DISPLAY RESULTS

if st.session_state.results:

    result = st.session_state.results

    # FINAL REPORT

    st.header("📝 Research Report")

    st.markdown(
        result.get("report", "No report generated.")
    )

    st.download_button(

        label="⬇ Download Report",

        data=result.get("report", ""),

        file_name="research_report.md",

        mime="text/markdown"
    )

    # CRITIQUE

    st.header("🧐 Critic Feedback")

    st.markdown(
        result.get(
            "critique",
            "No critique available."
        )
    )

    # OBSERVABILITY METRICS

    st.header("📊 Pipeline Observability")

    metrics = result.get("metrics", {})

    metric_rows = []

    for node, values in metrics.items():

        metric_rows.append({

            "Node": node,

            "Latency": values.get(
                "latency",
                0
            ),

            "Success": values.get(
                "success",
                False
            )
        })

    metrics_df = pd.DataFrame(
        metric_rows
    )

    st.dataframe(
        metrics_df,
        use_container_width=True
    )

    # AI EVALUATION

    st.header("🧠 AI Evaluation")

    evaluation = result.get(
        "evaluation",
        "No evaluation available"
    )

    # evaluation is STRING now
    st.markdown(evaluation)

    # SOURCES

    st.header("🌐 Sources")

    for url in result.get("sources", []):

        st.markdown(f"- {url}")

    # RAW SCRAPED CONTENT

    with st.expander(
        "📄 Raw Scraped Content"
    ):

        st.write(
            result.get(
                "scraped_content",
                ""
            )
        )

    # TOTAL RUNTIME

    st.success(
        f"Pipeline completed in "
        f"{result.get('total_runtime', 0)} seconds"
    )

# FOOTER

st.markdown("---")

st.caption(
    "Built by Harsh Kumar"
)