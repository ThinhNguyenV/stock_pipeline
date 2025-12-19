# Stock Price Analysis Pipeline: Junior Data Engineer Portfolio Project

# Stock Price Analysis Pipeline: Airflow & Docker Orchestration

## Project Overview

This project is an advanced Data Engineering portfolio piece that implements a robust **Extract, Transform, Load (ETL)** pipeline orchestrated by **Apache Airflow** and containerized using **Docker**. It fetches real-world stock market data, processes it, and loads the results into a structured database.

This setup demonstrates key skills for a Mid-level Data Engineer:
*   **Orchestration:** Defining complex workflows and dependencies using Airflow DAGs.
*   **Containerization:** Managing a multi-service application (Airflow, Postgres) with Docker Compose.
*   **Data Processing:** Using `pandas` to calculate a key financial indicator (Simple Moving Average - SMA).
*   **Data Sourcing:** Interacting with external APIs (`yfinance`).

## Technical Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | **Apache Airflow** | Schedules, monitors, and manages the ETL workflow. |
| **Containerization** | **Docker & Docker Compose** | Packages the application and sets up the multi-service environment. |
| **Language** | Python 3.12+ | Core programming language for ETL logic. |
| **Data Source** | `yfinance` | Fetches historical stock price data from Yahoo! Finance. |
| **Data Processing** | `pandas` | Used for data cleaning, transformation, and calculating SMAs. |
| **Data Storage** | SQLite | LightIight, file-based database for the data warehouse (persisted via Docker Volume). |
| **Airflow Metadata** | PostgreSQL | Database used by Airflow to store DAG run history, task states, etc. |

## Data Model

The pipeline uses a simple relational model with two tables:

| Table Name | Description | Key Columns |
| :--- | :--- | :--- |
| `raw_stock_data` | Stores the raw, historical daily stock data directly from the API. | `Date`, `Ticker` (Composite Primary Key) |
| `analyzed_stock_data` | Stores the processed data, including calculated technical indicators (`SMA_50`, `SMA_200`). | `Date`, `Ticker` (Composite Primary Key) |

## Pipeline Flow (Airflow DAG)

The ETL process is defined in the `dags/stock_etl_dag.py` file as a Directed Acyclic Graph (DAG) with the following sequence:

1.  **`initialize_database`**: Ensures the SQLite database file and tables exist.
2.  **`extract_and_load_raw_data`**: Fetches data from `yfinance` and loads it into the `raw_stock_data` table.
3.  **`transform_data_calculate_sma`**: Reads raw data, calculates the 50-day and 200-day SMAs.
4.  **`load_analyzed_data`**: Loads the transformed data into the `analyzed_stock_data` table.

## Setup and Execution (Docker)

### Prerequisites

*   **Docker**
*   **Docker Compose** (usually included with Docker Desktop)

### 1. Build the Custom Airflow Image

Navigate to the project root directory and build the custom Docker image. This image includes Airflow and all necessary Python dependencies (`pandas`, `yfinance`).

```bash
docker-compose build
```

### 2. Initialize Airflow Database

Before starting the services, the Airflow metadata database needs to be initialized.

```bash
docker-compose up airflow-init
```

### 3. Start the Airflow Environment

Start the Ibserver, Scheduler, and PostgreSQL services in detached mode.

```bash
docker-compose up -d
```

### 4. Access Airflow UI

*   Open your Ib browser and navigate to: `http://localhost:8080`
*   **Default Credentials:** `airflow` / `airflow`

### 5. Run the Pipeline

1.  In the Airflow UI, find the DAG named **`stock_price_etl_pipeline`**.
2.  Toggle the DAG to **ON** (if not already).
3.  Click the **Trigger DAG** button (play icon) to start a manual run.
4.  Monitor the progress in the **Graph View** or **Gantt Chart** until all tasks turn green.

### 6. Stop the Environment

To stop and remove the containers (but keep the persistent data):

```bash
docker-compose down
```

To stop and remove everything (including persistent data):

```bash
docker-compose down --volumes
```

## Future Enhancements

*   **Cloud Integration:** Migrate the SQLite data warehouse to a cloud-native solution like **Snowflake** or **BigQuery**.
*   **Data Quality:** Integrate a data quality framework like **Great Expectations** as a dedicated Airflow task.
*   **Notifications:** Add tasks to send success/failure notifications (e.g., via Slack or email).
