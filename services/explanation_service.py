# services/explanation_service.py

def explain_retry_pressure(metrics, risk_level, window_days):
    """
    Returns a human-readable explanation string
    """

    if not metrics:
        return (
            f"Not enough data to assess retry behavior over the last "
            f"{window_days} days."
        )

    baseline = metrics["baseline_avg"]
    recent = metrics["recent_avg"]
    delta = metrics["delta"]

    if risk_level == "STABLE":
        return (
            f"Retry behavior is stable. Average retries changed from "
            f"{baseline} to {recent} over the last {window_days} days, "
            f"which is within normal variation."
        )

    if risk_level == "DRIFTING":
        return (
            f"Retry pressure is increasing. Average retries rose from "
            f"{baseline} to {recent} over the last {window_days} days, "
            f"suggesting early signs of instability."
        )

    if risk_level == "DEGRADING":
        return (
            f"Retry pressure has increased significantly. Average retries "
            f"climbed from {baseline} to {recent} over the last "
            f"{window_days} days, indicating sustained system stress."
        )

    return (
        f"Retry behavior could not be classified due to insufficient or "
        f"unclear data over the last {window_days} days."
    )
