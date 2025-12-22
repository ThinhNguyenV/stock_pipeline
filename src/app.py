import streamlit as st
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import plotly.express as px

# Configuration
CASSANDRA_HOSTS = ['cassandra']
CASSANDRA_KEYSPACE = 'stock_keyspace'

@st.cache_resource
def get_cassandra_session():
    """Connects to the Cassandra cluster and returns a session."""
    try:
        cluster = Cluster(CASSANDRA_HOSTS)
        session = cluster.connect(CASSANDRA_KEYSPACE)
        session.row_factory = dict_factory
        return session
    except Exception as e:
        st.error(f"Could not connect to Cassandra: {e}")
        return None

def fetch_stock_data(session, ticker):
    """Fetches all historical data for a given ticker from Cassandra."""
    query = f"SELECT date, close, sma_50, sma_200 FROM stock_prices WHERE ticker = '{ticker}'"
    rows = session.execute(query)
    df = pd.DataFrame(rows)
    
    if df.empty:
        return pd.DataFrame()
        
    # Convert date to datetime object for plotting
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("Stock Price Analysis Dashboard (Cassandra + Streamlit)")
    
    session = get_cassandra_session()
    if session is None:
        st.stop()

    # Get a list of available tickers from Cassandra
    try:
        ticker_rows = session.execute("SELECT DISTINCT ticker FROM stock_prices")
        available_tickers = [row['ticker'] for row in ticker_rows]
    except Exception as e:
        st.error(f"Error fetching available tickers: {e}")
        available_tickers = ['AAPL', 'MSFT', 'GOOGL'] # Fallback
        
    if not available_tickers:
        st.warning("No data found in Cassandra. Please run the Airflow DAG first.")
        st.stop()

    # Sidebar for user selection
    st.sidebar.header("Select Stock")
    selected_ticker = st.sidebar.selectbox("Ticker Symbol", available_tickers)

    # Fetch and display data
    st.header(f"Historical Data for {selected_ticker}")
    
    data_load_state = st.text("Loading data from Cassandra...")
    df = fetch_stock_data(session, selected_ticker)
    data_load_state.text("Loading data... done!")

    if df.empty:
        st.warning(f"No data found for {selected_ticker} in Cassandra.")
        return

    # Display the raw data table
    if st.checkbox('Show raw data'):
        st.subheader('Raw Data')
        st.dataframe(df.tail(10))

    # Create the line chart
    st.subheader('Price and Moving Averages')
    
    # Melt the DataFrame for Plotly
    df_melt = df.melt(id_vars=['date'], value_vars=['close', 'sma_50', 'sma_200'], 
                      var_name='Metric', value_name='Value')
    
    fig = px.line(df_melt, x='date', y='Value', color='Metric', 
                  title=f'{selected_ticker} Closing Price and Moving Averages',
                  labels={'Value': 'Price (USD)', 'date': 'Date'})
    
    # Customize line colors
    fig.update_traces(
        line=dict(width=3),
        selector=dict(name='close')
    )
    fig.update_traces(
        line=dict(dash='dash', width=1),
        selector=dict(name='sma_50')
    )
    fig.update_traces(
        line=dict(dash='dot', width=1),
        selector=dict(name='sma_200')
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
