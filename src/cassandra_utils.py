import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Configuration
CASSANDRA_HOSTS = ['cassandra']
CASSANDRA_KEYSPACE = 'stock_keyspace'

def get_cassandra_session():
    """
    Connects to the Cassandra cluster and returns a session.
    Retries connection to wait for Cassandra service to be up.
    """
    max_retries = 10
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to Cassandra at {CASSANDRA_HOSTS} (Attempt {attempt + 1}/{max_retries})...")
            # In a docker-compose network, we can use the service name 'cassandra'
            cluster = Cluster(CASSANDRA_HOSTS)
            session = cluster.connect()
            print("Successfully connected to Cassandra.")
            return session
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            
    raise ConnectionError("Failed to connect to Cassandra after multiple retries.")

def initialize_cassandra_schema():
    """
    Creates the Keyspace and the stock_prices table.
    """
    session = get_cassandra_session()
    
    # 1. Create Keyspace
    print(f"Creating Keyspace {CASSANDRA_KEYSPACE} if it doesn't exist...")
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
    """)
    
    # 2. Set the Keyspace
    session.set_keyspace(CASSANDRA_KEYSPACE)
    
    # 3. Create Table
    print("Creating table stock_prices if it doesn't exist...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            ticker text,
            date date,
            close float,
            sma_50 float,
            sma_200 float,
            load_timestamp timestamp,
            PRIMARY KEY ((ticker), date)
        ) WITH CLUSTERING ORDER BY (date DESC)
    """)
    
    print("Cassandra schema initialized successfully.")
    session.shutdown()

# CQL for inserting data
INSERT_STOCK_PRICE_CQL = f"""
INSERT INTO {CASSANDRA_KEYSPACE}.stock_prices 
(ticker, date, close, sma_50, sma_200, load_timestamp)
VALUES (?, ?, ?, ?, ?, ?)
"""

def load_data_to_cassandra(transformed_df):
    """
    Loads the transformed DataFrame into the Cassandra stock_prices table.
    """
    if transformed_df.empty:
        print("Warning: Transformed DataFrame is empty. Skipping load.")
        return 0

    session = get_cassandra_session()
    session.set_keyspace(CASSANDRA_KEYSPACE)
    
    # Prepare the statement once
    prepared_stmt = session.prepare(INSERT_STOCK_PRICE_CQL)
    
    loaded_count = 0
    print("Starting data loading to Cassandra...")
    
    # Iterate over the DataFrame and execute the prepared statement
    for index, row in transformed_df.iterrows():
        # Filter out rows where SMA_200 is NaN
        if pd.isna(row['SMA_200']):
            continue
            
        try:
            # Data types must match the CQL definition: (text, date, float, float, float, timestamp)
            session.execute(prepared_stmt, (
                row['Ticker'],
                row['Date'], # Date is already a string 'YYYY-MM-DD' from transform.py
                row['Close'],
                row['SMA_50'],
                row['SMA_200'],
                datetime.now() # Use current time for load_timestamp
            ))
            loaded_count += 1
        except Exception as e:
            print(f"Error loading record for {row['Ticker']} on {row['Date']}: {e}")
            
    session.shutdown()
    print(f"Loading complete. {loaded_count} records loaded into Cassandra.")
    return loaded_count

if __name__ == "__main__":
    # Example usage for testing
    # initialize_cassandra_schema()
    pass
