# Junior Data Engineer Portfolio Project: Stock Price Analysis Pipeline

## 1. Project Goal
To build an end-to-end data pipeline that fetches real-world stock market data, performs data cleaning and transformation, calculates a key financial indicator (Simple Moving Average - SMA), and loads the structured data into a relational database. This project demonstrates proficiency in using external APIs, data processing with Pandas, and ETL/ELT principles.

## 2. Technology Stack
*   **Language:** Python 3.12+
*   **Data Source:** `yfinance` library (uses Yahoo! Finance API)
*   **Data Processing:** `pandas` (for data manipulation and calculations)
*   **Data Storage:** SQLite (for simplicity and portability)
*   **Orchestration:** Simple Python script

## 3. Data Model (Relational)

The database will contain two main tables:

### 1. `raw_stock_data` (Staging/Historical Data)
This table stores the raw, historical daily stock data fetched directly from the API.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Date` | TEXT (YYYY-MM-DD) | The trading date (Primary Key) |
| `Ticker` | TEXT | The stock symbol (e.g., AAPL, GOOG) (Primary Key) |
| `Open` | REAL | Opening price of the stock |
| `High` | REAL | Highest price of the stock |
| `Low` | REAL | LoIst price of the stock |
| `Close` | REAL | Closing price of the stock |
| `Volume` | INTEGER | Trading volume |

### 2. `analyzed_stock_data` (Transformed/Analyzed Data)
This table stores the processed data, including the calculated technical indicator.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Date` | TEXT (YYYY-MM-DD) | The trading date (Primary Key) |
| `Ticker` | TEXT | The stock symbol (Primary Key) |
| `Close` | REAL | Closing price of the stock |
| `SMA_50` | REAL | 50-Day Simple Moving Average (Calculated Metric) |
| `SMA_200` | REAL | 200-Day Simple Moving Average (Calculated Metric) |
| `Load_Timestamp` | TEXT | Timestamp of when the record was loaded (Audit Column) |

## 4. Pipeline Architecture and Steps

The pipeline will execute in three logical steps (ETL):

1.  **Extraction (`extract.py`):**
    *   Uses `yfinance` to download historical data for a list of tickers (e.g., AAPL, MSFT).
    *   Loads the raw data into the `raw_stock_data` table.
2.  **Transformation (`transform.py`):**
    *   Reads data from `raw_stock_data`.
    *   Calculates the 50-day and 200-day Simple Moving Averages (SMA) using Pandas.
    *   Prepares the final, structured data for loading.
3.  **Loading (`load.py`):**
    *   Loads the transformed data into the `analyzed_stock_data` table.
4.  **Orchestration (`main_pipeline.py`):**
    *   Executes the above scripts in the correct sequence.

## 5. Project Structure

```
junior_de_project/
├── dags/
│   └── stock_etl_dag.py        # Airflow DAG definition
├── src/
│   ├── __init__.py
│   ├── db_utils.py             # Postgres connection & initialization
│   ├── sql_definitions.py      # PostgreSQL DDL and DML queries
│   ├── extract.py              # yfinance extraction logic
│   ├── transform.py            # Pandas SMA calculations
│   └── load.py                 # Final load to Postgres
├── docker-compose.yaml         # Orchestration for Airflow, Postgres, & Redis
├── Dockerfile                  # Custom Airflow image with dependencies
├── requirements.txt            # Python dependencies (yfinance, psycopg2-binary, etc.)
└── STOCK_DESIGN.md             # This document
```
