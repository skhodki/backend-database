import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_db_connection():
    """Create and return a connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Test the connection if the script is run directly
if __name__ == "__main__":
    test_conn = get_db_connection()
    if test_conn:
        print("Success! Connected to PostgreSQL database.")
        test_conn.close()