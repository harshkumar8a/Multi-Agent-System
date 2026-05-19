import time


def track_metrics(
    node_name: str,
    start_time: float,
    success: bool = True
):

    latency = time.time() - start_time

    return {
        "node": node_name,
        "latency": round(latency, 2),
        "success": success
    }