import sqlite3
import os

DB_DIR = "database"
DB_FILE = os.path.join(DB_DIR, "offers.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                image_url TEXT,
                current_price REAL NOT NULL,
                last_sent_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_offer(offer_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM offers WHERE id = ?",
            (offer_id,)
        )
        return cur.fetchone()


def insert_offer(offer_id, offer):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO offers (id, title, url, image_url, current_price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            offer_id,
            offer["title"],
            offer["sourceUrl"],
            offer.get("image", {}).get("url"),
            offer["price"]
        ))


def update_price(offer_id, new_price):
    with get_connection() as conn:
        conn.execute("""
            UPDATE offers
            SET current_price = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_price, offer_id))


def mark_sent(offer_id, price):
    with get_connection() as conn:
        conn.execute("""
            UPDATE offers
            SET last_sent_price = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (price, offer_id))
