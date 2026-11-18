import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if not conn:
        raise SystemExit(1)

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("TRUNCATE events RESTART IDENTITY CASCADE;")
            cursor.execute("""
                SELECT e.event_id, e.title, e.event_date, e.status,
                       l.name AS location_name
                FROM events e
                LEFT JOIN locations l ON e.location_id = l.location_id
            """)
            rows = cursor.fetchall()
            print(rows)
        conn.commit()
    finally:
        conn.close()