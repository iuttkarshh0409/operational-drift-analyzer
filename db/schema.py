# db/schema.py
from db.connection import get_connection
from datetime import datetime

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drift_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_days INTEGER NOT NULL,
            analyzed_at TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            primary_signal TEXT NOT NULL,
            secondary_signal TEXT,
            explanation TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
