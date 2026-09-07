import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("commit_metrics.db")

def init_db() -> None:
    """Initializes the SQLite database and creates the audit_logs table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            overall_grade TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_audit_log(username: str, grade: str, score: float) -> None:
    """Saves a new audit record into the database with a UTC timestamp."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_logs (username, overall_grade, score, timestamp) VALUES (?, ?, ?, ?)",
        (username, grade, score, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def get_audit_history(username: str) -> list[dict]:
    """Retrieves all past audit logs for a specified GitHub username, ordered chronologically."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT overall_grade, score, timestamp FROM audit_logs WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"grade": r[0], "score": r[1], "timestamp": r[2]} for r in rows]