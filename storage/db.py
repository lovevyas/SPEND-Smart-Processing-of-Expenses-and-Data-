import sqlite3
import json
from datetime import datetime

DB_PATH = "spend.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type TEXT,
        merchant TEXT,
        amount REAL,
        currency TEXT,
        payment_method TEXT,
        source_account TEXT,
        wallet_id TEXT,
        items_json TEXT,
        date TEXT,
        time TEXT,
        confidence REAL,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_transaction(txn: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (
        document_type, merchant, amount, currency,
        payment_method, source_account, wallet_id,
        items_json, date, time, confidence, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        txn["document_type"],
        txn["merchant"],
        txn["amount"],
        txn["currency"],
        txn["payment_method"],
        txn["source_account"],
        txn["wallet_id"],
        json.dumps(txn["items"]),
        txn["date"],
        txn["time"],
        txn["confidence"],
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
