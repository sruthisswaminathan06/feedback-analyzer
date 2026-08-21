import sqlite3
from typing import List, Dict, Any

DB_NAME = "feedback.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review TEXT NOT NULL,
                label TEXT NOT NULL,
                score INTEGER NOT NULL,
                theme TEXT NOT NULL
            )
        """)
        conn.commit()

def save_results(review_data_list: List[Dict[str, Any]]):
    if not review_data_list:
        return

    records = [
        (item["review"], item["label"], item["score"], item["theme"])
        for item in review_data_list
    ]
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO feedback (review, label, score, theme)
            VALUES (?, ?, ?, ?)
        """, records)
        conn.commit()

def load_history() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, review, label, score, theme FROM feedback ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]