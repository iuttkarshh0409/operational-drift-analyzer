# app.py
from db.schema import init_db
from services.drift_metrics_service import (
    calculate_dead_event_ratio,
    calculate_retry_pressure
)
from services.risk_classifier import classify_retry_pressure
from services.explanation_service import explain_retry_pressure
from db.repositories.drift_repo import save_drift_snapshot

WINDOW_DAYS = 7


def run_analysis():
    init_db()

    # --- Compute metrics ---
    retry_metrics = calculate_retry_pressure(WINDOW_DAYS)
    dead_metrics = calculate_dead_event_ratio(WINDOW_DAYS)

    # --- Risk classification ---
    risk_level = classify_retry_pressure(
        retry_metrics["delta"] if retry_metrics else None
    )

    # --- Explanation ---
    explanation = explain_retry_pressure(
        retry_metrics,
        risk_level,
        WINDOW_DAYS
    )

    # --- Confidence (still intentionally conservative) ---
    confidence = retry_metrics.get("confidence", 0.0) if retry_metrics else 0.0

    # --- Persist snapshot ---
    save_drift_snapshot(
        window_days=WINDOW_DAYS,
        risk_level=risk_level,
        confidence=confidence,
        primary_signal="retry_pressure",
        secondary_signal=None,
        explanation=explanation,
        dead_event_ratio=dead_metrics.get("dead_ratio") if dead_metrics else None,
        dead_event_confidence=dead_metrics.get("confidence") if dead_metrics else None
    )

    # --- CLI output ---
    print("\nOperational Drift Analysis")
    print("-" * 30)
    print(f"Window       : {WINDOW_DAYS} days")
    print(f"Risk level   : {risk_level}")
    print(f"Confidence   : {confidence}")
    print(f"Explanation  : {explanation}")


if __name__ == "__main__":
    run_analysis()
