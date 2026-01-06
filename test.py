import sqlite3
conn = sqlite3.connect("../failure-aware-system/db/failure_aware.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM event_detected")
print(cursor.fetchone())
conn.close()

