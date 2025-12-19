import psycopg2
import os
# Import các câu lệnh SQL đã được bạn update cho Postgres
from src.sql_queries import ALL_CREATE_QUERIES 

def get_pg_connection():
    """Thiết lập kết nối tới Postgres database trong Docker."""
    return psycopg2.connect(
        host="postgres",           # Tên service trong docker-compose.yaml
        database="airflow",        # Tên DB mặc định
        user="airflow",
        password="airflow",
        port="5432"
    )

def initialize_database():
    """Kết nối tới Postgres và khởi tạo toàn bộ Schema (Ecommerce/Stock)."""
    print("Connecting to PostgreSQL to initialize schema...")
    conn = None
    try:
        # 1. Kết nối tới DB
        conn = get_pg_connection()
        cursor = conn.cursor()
        
        # 2. Thực thi từng câu lệnh CREATE TABLE
        # Đảm bảo ALL_CREATE_QUERIES đã sử dụng SERIAL và ON CONFLICT
        for query in ALL_CREATE_QUERIES:
            cursor.execute(query)
            
        # 3. Xác nhận thay đổi
        conn.commit()
        print("PostgreSQL database schema initialized successfully.")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"An error occurred during PostgreSQL initialization: {e}")
        raise 
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()