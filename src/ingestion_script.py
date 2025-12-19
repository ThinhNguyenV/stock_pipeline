import json
import sqlite3
import os
from datetime import datetime
from sql_queries import CREATE_RAW_TRANSACTIONS_TABLE, INSERT_RAW_TRANSACTION

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'warehouse', 'ecommerce_warehouse.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db(conn):
    """Creates the raw_transactions table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute(CREATE_RAW_TRANSACTIONS_TABLE)
    conn.commit()

def ingest_data(file_path):
    """Reads the raw JSON file and loads data into the raw_transactions table."""
    if not os.path.exists(file_path):
        print(f"Error: Raw data file not found at {file_path}")
        return

    conn = get_db_connection()
    initialize_db(conn)
    cursor = conn.cursor()
    
    print(f"Ingesting data from {file_path}...")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    ingested_count = 0
    for record in data:
        try:
            # Data to be inserted into raw_transactions table
            # (transaction_id, user_id, product_id, quantity, price, timestamp)
            transaction_data = (
                record['transaction_id'],
                record['user_details']['user_id'],
                record['product_details']['product_id'],
                record['quantity'],
                record['price'],
                record['timestamp']
            )
            cursor.execute(INSERT_RAW_TRANSACTION, transaction_data)
            ingested_count += 1
        except sqlite3.IntegrityError:
            print(f"Warning: Duplicate transaction_id {record['transaction_id']} skipped.")
        except Exception as e:
            print(f"Error ingesting record: {e}. Record: {record}")
            
    conn.commit()
    conn.close()
    print(f"Ingestion complete. {ingested_count} records loaded into raw_transactions.")
    
    return ingested_count

if __name__ == "__main__":
    # Example usage (requires a generated file)
    # This is for testing only, the main pipeline will call this function
    # ingest_data('../data/raw/transactions_20251218120000.json')
    pass
