import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from src.db_utils import get_pg_connection 
from src.sql_definitions import CREATE_RAW_STOCK_TABLE, INSERT_RAW_STOCK_DATA

TICKERS = ['AAPL', 'MSFT', 'GOOGL']

def initialize_db():
    conn = get_pg_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_RAW_STOCK_TABLE)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def fetch_and_load_data(tickers):
    initialize_db()
    conn = get_pg_connection()
    cursor = conn.cursor()
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365 * 2)).strftime('%Y-%m-%d')
    total_records_loaded = 0
    
    for ticker in tickers:
        print(f"Fetching {ticker} from {start_date} to {end_date}...")
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if data.empty:
                continue
            
            data = data.reset_index()
            data['Ticker'] = ticker
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            data_to_insert = data[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
            records = [tuple(x) for x in data_to_insert.values]
            
            cursor.executemany(INSERT_RAW_STOCK_DATA, records)
            conn.commit()
            
            print(f"Loaded {len(records)} records for {ticker}.")
            total_records_loaded += len(records)
            
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            conn.rollback()
            
    cursor.close()
    conn.close()
    return total_records_loaded