# services/risk_classifier.py

def classify_retry_pressure(delta):
    """
    Takes retry pressure delta (float)
    Returns one of: STABLE, DRIFTING, DEGRADING
    """

    if delta is None:
        return "UNKNOWN"

    if delta <= 0.2:
        return "STABLE"
    elif delta <= 0.6:
        return "DRIFTING"
    else:
        return "DEGRADING"
