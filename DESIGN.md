# Junior Data Engineer Portfolio Project: E-commerce Data Pipeline

## 1. Project Goal
To build a simplified, end-to-end data pipeline that simulates an e-commerce transaction flow, demonstrating core Data Engineering skills: data generation, ingestion, transformation (ETL/ELT), data modeling, and orchestration.

## 2. Technology Stack
*   **Language:** Python 3.11+
*   **Data Generation:** `faker` library
*   **Data Storage:** SQLite (for simplicity and portability; easily upgradeable to PostgreSQL or a cloud data warehouse like Snowflake/BigQuery)
*   **Data Processing:** Standard Python libraries (`csv`, `json`, `sqlite3`)
*   **Orchestration:** Simple Python script (easily upgradeable to Apache Airflow)

## 3. Data Model (Simplified Star Schema)

The database will contain two main types of tables: **Staging** (raw data) and **Dimensional** (modeled data).

### Staging Tables (Raw Data)
These tables hold the raw, untransformed data immediately after ingestion.

| Table Name | Description | Key Fields |
| :--- | :--- | :--- |
| `raw_transactions` | Raw event data simulating user purchases. | `transaction_id`, `user_id`, `product_id`, `quantity`, `price`, `timestamp` |

### Dimensional Tables (Modeled Data)
These tables are optimized for analytical queries.

| Table Name | Type | Description | Key Fields |
| :--- | :--- | :--- | :--- |
| `dim_users` | Dimension | Stores unique user information. | `user_key` (PK), `user_id` (Natural Key), `name`, `email`, `registration_date` |
| `dim_products` | Dimension | Stores unique product information. | `product_key` (PK), `product_id` (Natural Key), `name`, `category`, `unit_price` |
| `fact_orders` | Fact | Stores transaction metrics and foreign keys to dimensions. | `order_key` (PK), `transaction_id`, `user_key` (FK), `product_key` (FK), `quantity`, `total_amount`, `order_timestamp` |

## 4. Pipeline Architecture and Steps

The pipeline will execute in four logical steps:

1.  **Data Generation (`data_generator.py`):**
    *   Generates a batch of simulated e-commerce transaction events (JSON format).
    *   Writes the raw data to a file in the `/data/raw` directory.
2.  **Ingestion (`ingestion_script.py`):**
    *   Reads the raw JSON file from `/data/raw`.
    *   Loads the data into the `raw_transactions` staging table in the SQLite database.
3.  **Transformation (`transformation_script.py`):**
    *   **ETL Logic:** Reads data from `raw_transactions`.
    *   **Dimension Loading (SCD Type 1):** Extracts and loads new/updated users and products into `dim_users` and `dim_products`.
    *   **Fact Loading:** Joins the raw transactions with the newly generated dimension keys and loads the final, clean data into `fact_orders`.
4.  **Orchestration (`run_pipeline.py`):**
    *   Executes the above scripts in the correct sequence.

## 5. Project Structure

```
junior_de_project/
├── data/
│   ├── raw/
│   │   └── transactions_20251218.json  # Raw generated data
│   └── warehouse/
│       └── ecommerce_warehouse.db      # SQLite Database
├── src/
│   ├── __init__.py
│   ├── data_generator.py               # Step 1: Generates raw data
│   ├── ingestion_script.py             # Step 2: Loads raw data to staging
│   ├── transformation_script.py        # Step 3: Transforms and loads to DWH
│   ├── run_pipeline.py                 # Step 4: Orchestrates the entire flow
│   └── sql_queries.py                  # SQL definitions (CREATE TABLE, INSERT, etc.)
├── DESIGN.md                           # This document
└── README.md                           # Project overview and setup instructions
```
