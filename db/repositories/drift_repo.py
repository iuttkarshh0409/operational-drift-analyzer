# db/repositories/drift_repo.py
from db.connection import get_connection
from datetime import datetime, timezone


def save_drift_snapshot(
    window_days,
    risk_level,
    confidence,
    primary_signal,
    secondary_signal,
    explanation,
    dead_event_ratio,
    dead_event_confidence
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO drift_snapshots (
        window_days,
        analyzed_at,
        risk_level,
        confidence,
        primary_signal,
        secondary_signal,
        explanation,
        dead_event_ratio,
        dead_event_confidence
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    window_days,
    datetime.now(timezone.utc).isoformat(),
    risk_level,
    confidence,
    primary_signal,
    secondary_signal,
    explanation,
    dead_event_ratio,
    dead_event_confidence
))



    conn.commit()
    conn.close()

def fetch_latest_snapshot():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            window_days,
            analyzed_at,
            risk_level,
            confidence,
            primary_signal,
            secondary_signal,
            explanation,
            dead_event_ratio,
            dead_event_confidence
        FROM drift_snapshots
        ORDER BY analyzed_at DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "window_days": row[0],
        "analyzed_at": row[1],
        "risk_level": row[2],
        "confidence": row[3],
        "primary_signal": row[4],
        "secondary_signal": row[5],
        "explanation": row[6],
        "dead_event_ratio": row[7],
        "dead_event_confidence": row[8]
    }
