import sqlite3
import os

DB_PATH = "database/ratings.db"

def init_db():
    if not os.path.exists("database"):
        os.makedirs("database")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_path TEXT,
            rating INTEGER,
            feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_rating(video_path, rating, feedback):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO ratings (video_path, rating, feedback) VALUES (?, ?, ?)', (video_path, rating, feedback))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
