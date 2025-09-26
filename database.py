import sqlite3, os, time

SCHEMA = """
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    event_type TEXT,
    ip TEXT,
    count INTEGER,
    description TEXT,
    sample_line TEXT
);
"""

def connect_db(path):
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn

def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = connect_db(path)
    c = conn.cursor()
    c.executescript(SCHEMA)
    conn.commit()
    conn.close()

def insert_alert(path, timestamp, event_type, ip, count, description, sample_line):
    conn = connect_db(path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO alerts (timestamp, event_type, ip, count, description, sample_line) VALUES (?, ?, ?, ?, ?, ?);",
        (int(timestamp), event_type, ip, count, description, sample_line)
    )
    conn.commit()
    conn.close()

def get_alerts(path, limit=100):
    conn = connect_db(path)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, event_type, ip, count, description, sample_line FROM alerts ORDER BY timestamp DESC LIMIT ?;", (limit,))
    rows = c.fetchall()
    conn.close()
    # Convert timestamp to readable string in app template if desired
    return rows

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), "data", "securelog.db")
    init_db(db_path)
    print("Initialized DB at", db_path)
