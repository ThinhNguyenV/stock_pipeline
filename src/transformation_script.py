import psycopg2
from src.db_utils import get_pg_connection
from src.sql_queries import (
    ALL_CREATE_QUERIES,
    SELECT_RAW_TRANSACTIONS,
    INSERT_DIM_USER,
    INSERT_DIM_PRODUCT,
    SELECT_USER_KEY,
    SELECT_PRODUCT_KEY,
    INSERT_FACT_ORDER
)

def initialize_dwh(conn):
    cursor = conn.cursor()
    for query in ALL_CREATE_QUERIES:
        cursor.execute(query)
    conn.commit()

def extract_raw_data(conn):
    cursor = conn.cursor()
    cursor.execute(SELECT_RAW_TRANSACTIONS)
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def transform_and_load(raw_data):
    conn = get_pg_connection()
    initialize_dwh(conn)
    cursor = conn.cursor()
    
    print("Loading dimensions...")
    unique_users = {}
    unique_products = {}
    
    for row in raw_data:        
        u_id = row['user_id']
        p_id = row['product_id']
        
        if u_id not in unique_users:
            unique_users[u_id] = (u_id, f"User_{u_id[:8]}", f"u_{u_id[:8]}@example.com", "2025-01-01")
            
        if p_id not in unique_products:
            unique_products[p_id] = (p_id, f"Prod_{p_id[:8]}", "Category_A", 10.0)
            
    for user_data in unique_users.values():
        cursor.execute(INSERT_DIM_USER, user_data)
        
    for product_data in unique_products.values():
        cursor.execute(INSERT_DIM_PRODUCT, product_data)
        
    conn.commit()
    print(f"Dimensions loaded: {len(unique_users)} users, {len(unique_products)} products.")
    
    print("Loading facts...")
    loaded_count = 0
    for row in raw_data:
        try:
            cursor.execute(SELECT_USER_KEY, (row['user_id'],))
            user_key = cursor.fetchone()[0]
            
            cursor.execute(SELECT_PRODUCT_KEY, (row['product_id'],))
            product_key = cursor.fetchone()[0]
            
            total_amount = float(row['price']) * int(row['quantity'])
            
            fact_data = (
                row['transaction_id'],
                user_key,
                product_key,
                row['quantity'],
                total_amount,
                row['timestamp']
            )
            
            cursor.execute(INSERT_FACT_ORDER, fact_data)
            loaded_count += 1
            
        except Exception as e:
            print(f"Error loading record {row.get('transaction_id')}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Facts loaded: {loaded_count} records.")
    return loaded_count

def main():
    print("Starting ETL process...")
    try:
        conn = get_pg_connection()
        raw_data = extract_raw_data(conn)
        conn.close()
        
        if not raw_data:
            print("No data found. Exiting.")
            return
            
        transform_and_load(raw_data)
        print("ETL pipeline finished successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()