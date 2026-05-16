# src/database.py
"""
Database connection and operations
"""

import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

def get_connection():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG)

def get_review_count():
    """Get total review count from database"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reviews")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def get_bank_summary():
    """Get summary by bank"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.bank_name, COUNT(r.review_id), AVG(r.rating)
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results