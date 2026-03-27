import psycopg2
from config import DB_CONFIG


def get_connection():
    """Create and return a new database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Could not connect to database: {e}")
        return None


def test_connection():
    """Quick test to verify the DB is reachable."""
    conn = get_connection()
    if conn:
        print("[OK] Connected to PostgreSQL successfully.")
        conn.close()
    else:
        print("[FAIL] Connection failed.")


if __name__ == "__main__":
    test_connection()
