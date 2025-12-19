import psycopg2
from src.sql_definitions import ALL_CREATE_QUERIES

def get_pg_connection():
    return psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow",
        port="5432"
    )

def initialize_database():
    conn = None
    try:
        conn = get_pg_connection()
        cursor = conn.cursor()
        for query in ALL_CREATE_QUERIES:
            cursor.execute(query)
        conn.commit()
        print("Schema initialized successfully.")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Initialization error: {e}")
        raise
    finally:
        if conn:
            conn.close()