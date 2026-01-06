from db.connection import get_connection


def migrate_add_dead_event_fields():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(drift_snapshots);")
    columns = [row[1] for row in cursor.fetchall()]

    if "dead_event_ratio" not in columns:
        cursor.execute("""
            ALTER TABLE drift_snapshots
            ADD COLUMN dead_event_ratio REAL;
        """)

    if "dead_event_confidence" not in columns:
        cursor.execute("""
            ALTER TABLE drift_snapshots
            ADD COLUMN dead_event_confidence REAL;
        """)

    conn.commit()
    conn.close()
