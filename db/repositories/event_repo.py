# db/repositories/event_repo.py
import sqlite3

FAILURE_DB_PATH = r"C:\Users\dubey\Desktop\Personal Vault\Projects\failure-aware-system\db\failure_aware.db"

def get_connection():
    return sqlite3.connect(FAILURE_DB_PATH)


# ----------------------------------------------------------
# Generic / Admin
# ----------------------------------------------------------
def fetch_events_in_range(start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sync_status, retry_count, detected_at
        FROM event_detected
        WHERE detected_at BETWEEN datetime(?) AND datetime(?)
    """, (start_date, end_date))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "sync_status": r[1],
            "retry_count": r[2],
            "detected_at": r[3],
        }
        for r in rows
    ]


# ----------------------------------------------------------
# Drift Metrics
# ----------------------------------------------------------
def fetch_retry_counts(start_ts, end_ts):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT retry_count
        FROM event_detected
        WHERE detected_at BETWEEN datetime(?) AND datetime(?)
    """, (start_ts, end_ts))

    rows = cursor.fetchall()
    conn.close()

    return [r[0] for r in rows]


def fetch_dead_event_count(start_ts, end_ts):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM event_detected
        WHERE sync_status = 'DEAD'
        AND detected_at BETWEEN datetime(?) AND datetime(?)
    """, (start_ts, end_ts))

    count = cursor.fetchone()[0]
    conn.close()
    return count


def fetch_total_event_count(start_ts, end_ts):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM event_detected
        WHERE detected_at BETWEEN datetime(?) AND datetime(?)
    """, (start_ts, end_ts))

    count = cursor.fetchone()[0]
    conn.close()
    return count
