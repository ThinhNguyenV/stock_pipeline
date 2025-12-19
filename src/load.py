import pandas as pd
from datetime import datetime
from src.db_utils import get_pg_connection
from src.sql_definitions import (
    CREATE_ANALYZED_STOCK_TABLE, 
    INSERT_ANALYZED_STOCK_DATA
)

def initialize_analyzed_table():
    conn = get_pg_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_ANALYZED_STOCK_TABLE)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def load_data(transformed_df):
    if transformed_df is None or transformed_df.empty:
        print("Warning: Transformed DataFrame is empty. Skipping load.")
        return 0

    initialize_analyzed_table()
    
    conn = get_pg_connection()
    cursor = conn.cursor()
    
    try:
        print("Starting data loading into Postgres...")
        
        load_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transformed_df['Load_Timestamp'] = load_timestamp
        
        # Select columns matching the INSERT_ANALYZED_STOCK_DATA schema
        records_df = transformed_df[['Date', 'Ticker', 'Close', 'SMA_50', 'SMA_200', 'Load_Timestamp']]
        
        # Filter out rows with NaN in SMA columns to ensure data quality
        # Postgres expects None instead of NaN for NULL values
        records_df = records_df.dropna(subset=['SMA_50', 'SMA_200'])
        
        if records_df.empty:
            print("Warning: No valid records after filtering. Skipping load.")
            return 0
            
        records = [tuple(x) for x in records_df.values]
        
        cursor.executemany(INSERT_ANALYZED_STOCK_DATA, records)
        conn.commit()
        
        print(f"Loading complete. {len(records)} records loaded.")
        return len(records)

    except Exception as e:
        print(f"Error loading data to Postgres: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()