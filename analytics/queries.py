import sqlite3

DB_PATH = "spend.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def total_spend_by_date(date: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE date = ?
    """, (date,))

    result = cursor.fetchone()[0]
    conn.close()

    return result or 0.0

def spend_by_merchant():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT merchant, SUM(amount) as total
    FROM transactions
    GROUP BY merchant
    ORDER BY total DESC
    """)

    results = cursor.fetchall()
    conn.close()

    return results

def spend_by_wallet():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT wallet_id, SUM(amount) as total
    FROM transactions
    WHERE wallet_id IS NOT NULL
    GROUP BY wallet_id
    """)

    results = cursor.fetchall()
    conn.close()

    return results

def high_confidence_spend(threshold=0.8):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE confidence >= ?
    """, (threshold,))

    result = cursor.fetchone()[0]
    conn.close()

    return result or 0.0
