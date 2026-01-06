# scripts/seed_events.py
from datetime import datetime, timedelta, timezone
import sqlite3
from pathlib import Path

# Absolute, deterministic path
DB_PATH = r"C:\Users\dubey\Desktop\Personal Vault\Projects\failure-aware-system\db\failure_aware.db"

def seed_events(days_back=30, events_per_day=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now(timezone.utc)

    seeded = 0

    for day in range(days_back, 7, -1):  # ensure baseline exists
        event_date = now - timedelta(days=day)

        for i in range(events_per_day):
            detected_at = event_date.replace(
                hour=10 + i,
                minute=0,
                second=0,
                microsecond=0
            )

            retry_count = (i % 4)  # realistic retry pattern

            cursor.execute("""
                INSERT INTO event_detected (
                    event_type,
                    event_payload,
                    detected_at,
                    sync_status,
                    retry_count,
                    source
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "SYNC_ATTEMPT",
                '{"seeded": true}',
                detected_at.isoformat(),
                "FAILED" if retry_count > 0 else "SYNCED",
                retry_count,
                "SEED"
            ))

            seeded += 1

    conn.commit()
    conn.close()

    print(f"Seeded {seeded} historical events.")

if __name__ == "__main__":
    seed_events()
