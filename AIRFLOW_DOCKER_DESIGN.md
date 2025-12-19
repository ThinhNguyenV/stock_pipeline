# Stock Price Analysis Pipeline: Airflow & Docker Upgrade

## 1. Upgrade Goal
To transform the existing Python-based ETL pipeline into a production-ready, containerized solution using **Apache Airflow** for orchestration and **Docker** for environment management. This demonstrates advanced Data Engineering skills in deployment, scheduling, and dependency management.

## 2. New Technology Stack
*   **Orchestration:** Apache Airflow (via Docker Compose)
*   **Containerization:** Docker, Docker Compose
*   **Database:** PostgreSQL (Airflow Metadata), SQLite (Data Warehouse - kept for simplicity, but easily swapped for a containerized Postgres/MySQL)
*   **ETL Code:** Python, Pandas, yfinance

## 3. Directory Structure

The project structure will be modified to accommodate Airflow's requirements:

```
stock_pipeline_project/
├── dags/                       # Airflow DAGs go here
│   └── stock_etl_dag.py        # The main Airflow pipeline definition
├── data/                       # Persistent data (SQLite DB, logs)
│   └── stock_warehouse.db
├── src/                        # Core Python ETL logic (extract.py, transform.py, load.py)
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── sql_definitions.py
├── Dockerfile                  # Defines the custom Python environment for Airflow workers
├── docker-compose.yaml         # Defines Airflow services (Ibserver, Scheduler, Postgres)
├── requirements.txt            # Python dependencies (pandas, yfinance, apache-airflow)
├── AIRFLOW_DOCKER_DESIGN.md    # This document
└── README.md                   # Updated setup instructions
```

## 4. Airflow DAG Design

The Airflow DAG will define the following sequential tasks:

| Task ID | Operator | Description | Maps to Original Script |
| :--- | :--- | :--- | :--- |
| `initialize_db` | PythonOperator | Ensures the SQLite database file and tables exist. | `main_pipeline.py` (Initialization) |
| `extract_data` | PythonOperator | Fetches data from `yfinance` and loads it into the `raw_stock_data` table. | `src/extract.py` |
| `transform_data` | PythonOperator | Reads raw data, calculates SMAs, and prepares the final dataset. | `src/transform.py` |
| `load_data` | PythonOperator | Loads the transformed data into the `analyzed_stock_data` table. | `src/load.py` |

## 5. Docker Strategy

1.  **`Dockerfile`**: A custom image will be built based on the official Airflow base image. This image will install the project's dependencies (`pandas`, `yfinance`) and copy the `src/` directory into the container's environment.
2.  **`docker-compose.yaml`**: This file will define the multi-container application:
    *   `postgres`: Airflow's metadata database.
    *   `Ibserver`: Airflow UI.
    *   `scheduler`: Airflow's task scheduler.
    *   `worker`: Executes the DAG tasks (using the custom image).
    *   Volumes will be used to persist the DAGs, logs, and the SQLite data file.
