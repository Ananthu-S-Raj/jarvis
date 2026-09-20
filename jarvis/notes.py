"""Small local SQLite note store."""

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "jarvis.db"


def _connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    return db


def add_note(text: str) -> str:
    with _connect() as db:
        db.execute("INSERT INTO notes(text) VALUES (?)", (text,))
    return "Note saved."


def recent_notes(limit: int = 5) -> list[str]:
    with _connect() as db:
        rows = db.execute(
            "SELECT text FROM notes ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [row[0] for row in rows]
