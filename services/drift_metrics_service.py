# services/drift_metrics_service.py
from datetime import datetime, timedelta, timezone
from db.repositories.event_repo import fetch_retry_counts


def calculate_retry_pressure(window_days=7):
    now = datetime.now(timezone.utc)

    recent_start = now - timedelta(days=window_days)
    baseline_start = recent_start - timedelta(days=window_days)

    baseline_retries = fetch_retry_counts(
        baseline_start.isoformat(),
        recent_start.isoformat()
    )

    recent_retries = fetch_retry_counts(
        recent_start.isoformat(),
        now.isoformat()
    )

    # -------- CASE 1: Absolutely no usable data --------
    if not baseline_retries and not recent_retries:
        return {
            "status": "NO_DATA",
            "baseline_avg": None,
            "recent_avg": None,
            "delta": None,
            "confidence": 0.0
        }

    # -------- CASE 2: System warming up (no baseline yet) --------
    if not baseline_retries:
        recent_avg = (
            round(sum(recent_retries) / len(recent_retries), 2)
            if recent_retries else 0
        )

        confidence = min(len(recent_retries), window_days) / window_days

        return {
            "status": "WARMUP",
            "baseline_avg": None,
            "recent_avg": recent_avg,
            "delta": None,
            "confidence": round(confidence, 2)
        }

    # -------- CASE 3: Valid comparison (this is the happy path) --------
    baseline_avg = sum(baseline_retries) / len(baseline_retries)
    recent_avg = sum(recent_retries) / len(recent_retries) if recent_retries else 0

    delta = recent_avg - baseline_avg

    confidence = min(
        len(baseline_retries),
        len(recent_retries),
        window_days
    ) / window_days

    return {
        "status": "OK",
        "baseline_avg": round(baseline_avg, 2),
        "recent_avg": round(recent_avg, 2),
        "delta": round(delta, 2),
        "confidence": round(confidence, 2)
    }
