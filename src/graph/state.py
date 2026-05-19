from typing import TypedDict, Dict, List


class ResearchState(TypedDict):

    topic: str

    search_results: str

    scraped_content: str

    report: str

    critique: str

    sources: List[str]

    metrics: Dict