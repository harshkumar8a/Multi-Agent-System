from langchain.tools import tool
from langsmith import traceable
from dotenv import load_dotenv

from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document

import requests
import trafilatura
import logging
import time
import os
import re
from typing import Dict, Any

load_dotenv()

# LangSmith Configuration

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "travel-agent-observability"


# Logging Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# Tavily Client

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# Utility Functions

def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """

    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def build_metrics(
    tool_name: str,
    latency: float,
    success: bool,
    extra: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Standardized observability metrics.
    """

    metrics = {
        "tool_name": tool_name,
        "latency_seconds": round(latency, 3),
        "success": success,
        "timestamp": time.time()
    }

    if extra:
        metrics.update(extra)

    return metrics


# WEB SEARCH TOOL

@tool
@traceable(name="web_search_tool")
def web_search(query: str) -> Dict[str, Any]:
    """
    Search the web for recent and reliable information.

    Returns:
    - Titles
    - URLs
    - Snippets
    - Observability metrics
    """

    start_time = time.time()

    logger.info(f"WEB SEARCH STARTED | Query: {query}")

    try:

        results = tavily.search(
            query=query,
            max_results=5
        )

        formatted_results = []

        for r in results["results"]:

            formatted_results.append({
                "title": r["title"],
                "url": r["url"],
                "snippet": r["content"][:300]
            })

        latency = time.time() - start_time

        metrics = build_metrics(
            tool_name="web_search",
            latency=latency,
            success=True,
            extra={
                "query": query,
                "results_count": len(formatted_results)
            }
        )

        logger.info(
            f"WEB SEARCH SUCCESS | "
            f"Results: {len(formatted_results)} | "
            f"Latency: {latency:.2f}s"
        )

        return {
            "status": "success",
            "data": formatted_results,
            "metrics": metrics
        }

    except Exception as e:

        latency = time.time() - start_time

        logger.exception("WEB SEARCH FAILED")

        metrics = build_metrics(
            tool_name="web_search",
            latency=latency,
            success=False,
            extra={
                "query": query,
                "error": str(e)
            }
        )

        return {
            "status": "error",
            "error": str(e),
            "metrics": metrics
        }


# SCRAPE URL TOOL

@tool
@traceable(name="scrape_url_tool")
def scrape_url(url: str) -> Dict[str, Any]:
    """
    Scrape and extract clean readable content from a URL.

    Observability Features:
    - Latency tracking
    - Extraction strategy tracking
    - Error monitoring
    - Content quality monitoring
    - Success/failure metrics
    """

    start_time = time.time()

    logger.info(f"SCRAPING STARTED | URL: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:

        # ====================================================
        # FETCH PAGE
        # ====================================================

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        logger.info(
            f"PAGE FETCHED | "
            f"Status: {response.status_code}"
        )

        # ====================================================
        # STRATEGY 1 → TRAFILATURA
        # ====================================================

        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:

            cleaned = clean_text(extracted)

            latency = time.time() - start_time

            metrics = build_metrics(
                tool_name="scrape_url",
                latency=latency,
                success=True,
                extra={
                    "url": url,
                    "strategy": "trafilatura",
                    "content_length": len(cleaned),
                    "status_code": response.status_code
                }
            )

            logger.info(
                f"SCRAPING SUCCESS | "
                f"Strategy: trafilatura | "
                f"Length: {len(cleaned)} | "
                f"Latency: {latency:.2f}s"
            )

            return {
                "status": "success",
                "content": cleaned[:5000],
                "metrics": metrics
            }

        # STRATEGY 2 → READABILITY

        doc = Document(html)

        clean_html = doc.summary()

        soup = BeautifulSoup(
            clean_html,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        if text and len(text.strip()) > 200:

            cleaned = clean_text(text)

            latency = time.time() - start_time

            metrics = build_metrics(
                tool_name="scrape_url",
                latency=latency,
                success=True,
                extra={
                    "url": url,
                    "strategy": "readability",
                    "content_length": len(cleaned),
                    "status_code": response.status_code
                }
            )

            logger.info(
                f"SCRAPING SUCCESS | "
                f"Strategy: readability | "
                f"Length: {len(cleaned)} | "
                f"Latency: {latency:.2f}s"
            )

            return {
                "status": "success",
                "content": cleaned[:5000],
                "metrics": metrics
            }

        # STRATEGY 3 → BEAUTIFULSOUP FALLBACK

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        cleaned = clean_text(text)

        if cleaned:

            latency = time.time() - start_time

            metrics = build_metrics(
                tool_name="scrape_url",
                latency=latency,
                success=True,
                extra={
                    "url": url,
                    "strategy": "beautifulsoup_fallback",
                    "content_length": len(cleaned),
                    "status_code": response.status_code
                }
            )

            logger.info(
                f"SCRAPING SUCCESS | "
                f"Strategy: fallback | "
                f"Length: {len(cleaned)} | "
                f"Latency: {latency:.2f}s"
            )

            return {
                "status": "success",
                "content": cleaned[:5000],
                "metrics": metrics
            }

        # NO CONTENT FOUND

        latency = time.time() - start_time

        metrics = build_metrics(
            tool_name="scrape_url",
            latency=latency,
            success=False,
            extra={
                "url": url,
                "reason": "No meaningful content found"
            }
        )

        return {
            "status": "error",
            "error": "Could not extract meaningful content.",
            "metrics": metrics
        }

    # TIMEOUT ERROR

    except requests.exceptions.Timeout:

        latency = time.time() - start_time

        logger.exception("SCRAPING TIMEOUT")

        metrics = build_metrics(
            tool_name="scrape_url",
            latency=latency,
            success=False,
            extra={
                "url": url,
                "error_type": "timeout"
            }
        )

        return {
            "status": "error",
            "error": "Request timed out.",
            "metrics": metrics
        }

    # HTTP ERROR

    except requests.exceptions.HTTPError as e:

        latency = time.time() - start_time

        logger.exception("HTTP ERROR")

        metrics = build_metrics(
            tool_name="scrape_url",
            latency=latency,
            success=False,
            extra={
                "url": url,
                "error_type": "http_error",
                "error": str(e)
            }
        )

        return {
            "status": "error",
            "error": str(e),
            "metrics": metrics
        }

    # GENERIC ERROR

    except Exception as e:

        latency = time.time() - start_time

        logger.exception("SCRAPING FAILED")

        metrics = build_metrics(
            tool_name="scrape_url",
            latency=latency,
            success=False,
            extra={
                "url": url,
                "error_type": "generic_error",
                "error": str(e)
            }
        )

        return {
            "status": "error",
            "error": str(e),
            "metrics": metrics
        }