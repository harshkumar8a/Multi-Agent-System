import re
from typing import Dict, List


# REPORT QUALITY EVALUATOR

def evaluate_report_quality(report: str) -> Dict:
    """
    Evaluate overall report quality.
    """

    score = 0

    checks = {
        "has_introduction": False,
        "has_key_findings": False,
        "has_conclusion": False,
        "sufficient_length": False,
        "professional_structure": False
    }

    report_lower = report.lower()

    # Section Checks

    if "introduction" in report_lower:
        checks["has_introduction"] = True
        score += 2

    if (
        "key findings" in report_lower
        or "findings" in report_lower
    ):
        checks["has_key_findings"] = True
        score += 2

    if "conclusion" in report_lower:
        checks["has_conclusion"] = True
        score += 2

    # Length Check

    word_count = len(report.split())

    if word_count > 500:
        checks["sufficient_length"] = True
        score += 2

    # Structure Check

    headers = re.findall(
        r"\n#+\s",
        report
    )

    if len(headers) >= 3:
        checks["professional_structure"] = True
        score += 2

    return {
        "quality_score": score,
        "max_score": 10,
        "checks": checks,
        "word_count": word_count
    }


# SOURCE COVERAGE EVALUATOR

def evaluate_source_coverage(
    sources: List[str]
) -> Dict:
    """
    Evaluate source diversity and coverage.
    """

    unique_sources = list(set(sources))

    return {

        "total_sources": len(sources),

        "unique_sources": len(unique_sources),

        "source_diversity_score": min(
            len(unique_sources),
            10
        )
    }


# CONTENT COMPLETENESS EVALUATOR

def evaluate_content_completeness(
    scraped_content: str
) -> Dict:
    """
    Evaluate completeness of scraped content.
    """

    word_count = len(
        scraped_content.split()
    )

    completeness = "LOW"

    if word_count > 300:
        completeness = "MEDIUM"

    if word_count > 1000:
        completeness = "HIGH"

    return {

        "scraped_word_count": word_count,

        "content_completeness": completeness
    }


# LATENCY EVALUATOR

def evaluate_latency(metrics: Dict) -> Dict:
    """
    Evaluate total pipeline latency.
    """

    total_latency = 0

    slow_nodes = []

    for key, value in metrics.items():

        if isinstance(value, dict):

            latency = value.get(
                "latency",
                0
            )

            total_latency += latency

            if latency > 10:
                slow_nodes.append(key)

    return {

        "total_latency": round(
            total_latency,
            2
        ),

        "slow_nodes": slow_nodes,

        "pipeline_performance": (
            "GOOD"
            if total_latency < 30
            else "SLOW"
        )
    }


# HALLUCINATION RISK EVALUATOR

def evaluate_hallucination_risk(
    report: str,
    scraped_content: str
) -> Dict:
    """
    Basic hallucination detection.
    """

    report_words = set(
        report.lower().split()
    )

    source_words = set(
        scraped_content.lower().split()
    )

    unsupported_words = report_words - source_words

    hallucination_ratio = (
        len(unsupported_words)
        /
        max(len(report_words), 1)
    )

    risk = "LOW"

    if hallucination_ratio > 0.4:
        risk = "MEDIUM"

    if hallucination_ratio > 0.6:
        risk = "HIGH"

    return {

        "hallucination_ratio": round(
            hallucination_ratio,
            2
        ),

        "hallucination_risk": risk
    }


# FINAL PIPELINE EVALUATOR

def evaluate_pipeline(state: Dict) -> Dict:
    """
    Complete pipeline evaluation.
    """

    report_eval = evaluate_report_quality(
        state["report"]
    )

    source_eval = evaluate_source_coverage(
        state["sources"]
    )

    completeness_eval = (
        evaluate_content_completeness(
            state["scraped_content"]
        )
    )

    latency_eval = evaluate_latency(
        state["metrics"]
    )

    hallucination_eval = (
        evaluate_hallucination_risk(
            state["report"],
            state["scraped_content"]
        )
    )

    final_score = (
        report_eval["quality_score"]
        +
        source_eval["source_diversity_score"]
    ) / 2

    return {

        "final_pipeline_score": round(
            final_score,
            2
        ),

        "report_evaluation": report_eval,

        "source_evaluation": source_eval,

        "content_evaluation": completeness_eval,

        "latency_evaluation": latency_eval,

        "hallucination_evaluation": hallucination_eval
    }