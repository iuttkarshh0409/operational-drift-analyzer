# app.py
from db.schema import init_db
from services.drift_metrics_service import calculate_retry_pressure
from services.risk_classifier import classify_retry_pressure
from services.explanation_service import explain_retry_pressure
from db.repositories.drift_repo import save_drift_snapshot

WINDOW_DAYS = 7

def run_analysis():
    init_db()

    metrics = calculate_retry_pressure(WINDOW_DAYS)
    risk_level = classify_retry_pressure(
        metrics["delta"] if metrics else None
    )

    explanation = explain_retry_pressure(
        metrics,
        risk_level,
        WINDOW_DAYS
    )

    confidence = 0.5 if metrics else 0.0  # honest placeholder

    save_drift_snapshot(
        window_days=WINDOW_DAYS,
        risk_level=risk_level,
        confidence=confidence,
        primary_signal="retry_pressure",
        secondary_signal=None,
        explanation=explanation,
        dead_event_ratio=metrics.get("dead_event_ratio") if metrics else None,
        dead_event_confidence=metrics.get("dead_event_confidence") if metrics else None
    )

    print("\nOperational Drift Analysis")
    print("-" * 30)
    print(f"Window       : {WINDOW_DAYS} days")
    print(f"Risk level   : {risk_level}")
    print(f"Confidence   : {confidence}")
    print(f"Explanation  : {explanation}")

if __name__ == "__main__":
    run_analysis()  



