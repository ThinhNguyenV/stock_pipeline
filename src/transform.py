import pandas as pd
from src.db_utils import get_pg_connection
from src.sql_definitions import SELECT_RAW_STOCK_DATA

TICKERS = ['AAPL', 'MSFT', 'GOOGL']

def calculate_sma(df, window):
    df = df.sort_values(by='Date')
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    return df

def transform_data():
    all_transformed_data = pd.DataFrame()
    conn = get_pg_connection()
    
    print("Starting data transformation...")
    
    try:
        for ticker in TICKERS:
            print(f"Processing {ticker}...")
            
            # Using pandas read_sql with %s placeholder for Postgres
            df = pd.read_sql_query(SELECT_RAW_STOCK_DATA, conn, params=(ticker,))
            
            if df.empty:
                print(f"Warning: No data for {ticker}. Skipping.")
                continue
            
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Technical Indicators
            df = calculate_sma(df, 50)
            df = calculate_sma(df, 200)
            
            transformed_df = df[['Date', 'Ticker', 'Close', 'SMA_50', 'SMA_200']].copy()
            transformed_df['Date'] = transformed_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            all_transformed_data = pd.concat([all_transformed_data, transformed_df], ignore_index=True)
            
    except Exception as e:
        print(f"Transformation error: {e}")
        raise
    finally:
        conn.close()
        
    print("Transformation complete.")
    return all_transformed_data