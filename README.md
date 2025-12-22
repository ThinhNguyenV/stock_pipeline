# Advanced Data Platform: Cassandra, Streamlit, Prometheus, Airflow & Docker

## Project Overview

This project is a **full-stack Data Platform** demonstrating advanced Data Engineering and DevOps skills. It transforms the stock price ETL pipeline into a robust, multi-service architecture using modern, distributed technologies.

### Key Features Demonstrated:

*   **Real-time Data Serving:** Migrated from SQLite to **Apache Cassandra** (NoSQL, distributed database) for time-series data storage.
*   **Interactive Visualization:** Added a **Streamlit** application to query Cassandra and display stock price charts and Moving Averages.
*   **Observability/Monitoring:** Integrated **Prometheus** and **Grafana** to monitor the health and performance of the Docker containers.
*   **Orchestration:** **Apache Airflow** schedules the ELT (Extract, Load, Transform) process.
*   **Containerization:** **Docker Compose** manages all 7 services (Airflow, Postgres, Cassandra, Streamlit, Prometheus, Grafana).

## Technical Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | Apache Airflow | Schedules the ELT workflow. |
| **Data Storage** | **Apache Cassandra** | High-availability, time-series NoSQL database. |
| **Visualization** | **Streamlit** | Interactive web application for data display. |
| **Monitoring** | **Prometheus** | Collects metrics from all services. |
| **Dashboard** | **Grafana** | Visualizes monitoring metrics (from Prometheus) and potentially data (from Cassandra). |
| **ETL Logic** | Python, Pandas, yfinance | Core data processing. |
| **Containerization** | Docker & Docker Compose | Manages the multi-service environment. |

## Pipeline Flow (ELT with Cassandra)

The ETL process is defined in the `dags/stock_etl_dag.py` file:

1.  **`initialize_cassandra_schema`**: Creates the Cassandra Keyspace and the `stock_prices` table.
2.  **`extract_data_from_yfinance`**: Fetches raw data from `yfinance` and passes it as a Pandas DataFrame via XCom.
3.  **`transform_data_calculate_sma`**: Calculates the 50-day and 200-day SMAs on the DataFrame (from XCom).
4.  **`load_analyzed_data_to_cassandra`**: Loads the final, transformed data into the Cassandra `stock_prices` table.

## Setup and Execution

### Prerequisites

*   **Docker**
*   **Docker Compose** (usually included with Docker Desktop)

### 1. Build the Custom Airflow Image

Navigate to the project root directory and build the custom Docker image. This image includes Airflow and all necessary Python dependencies (`pandas`, `yfinance`, `cassandra-driver`, `streamlit`).

```bash
docker-compose build
```

### 2. Initialize Airflow Database

Before starting the services, the Airflow metadata database needs to be initialized.

```bash
docker-compose up airflow-init
```

### 3. Start the Full Environment

Start all 7 services (Postgres, Cassandra, Airflow Webserver, Scheduler, Streamlit, Prometheus, Grafana) in detached mode.

```bash
docker-compose up -d
```

### 4. Access Services

| Service | URL | Credentials |
| :--- | :--- | :--- |
| **Airflow UI** | `http://localhost:8080` | `airflow` / `airflow` |
| **Streamlit App** | `http://localhost:8501` | N/A |
| **Prometheus UI** | `http://localhost:9090` | N/A |
| **Grafana UI** | `http://localhost:3000` | `admin` / `admin` (will prompt for new password) |

### 5. Run the Pipeline (Airflow)

1.  Access the **Airflow UI** (`http://localhost:8080`).
2.  Find the DAG named **`stock_price_etl_pipeline`**.
3.  Toggle the DAG to **ON**.
4.  Click the **Trigger DAG** button to start the ELT process.
5.  Monitor the tasks until they complete successfully, loading data into Cassandra.

### 6. View Visualization (Streamlit)

1.  Access the **Streamlit App** (`http://localhost:8501`).
2.  Select a Ticker from the sidebar.
3.  The chart will display the historical stock price and the calculated Moving Averages, querying the data directly from the Cassandra container.

### 7. Monitor Health (Prometheus/Grafana)

1.  Access the **Grafana UI** (`http://localhost:3000`).
2.  Configure a Prometheus data source pointing to `http://prometheus:9090`.
3.  Import a pre-built Docker/cAdvisor dashboard (e.g., ID 14285) to visualize the health of all running containers.

### 8. Stop the Environment

To stop and remove the containers:

```bash
docker-compose down
```

## Future Enhancements

*   **Cloud Deployment:** See the attached `CLOUD_DEPLOYMENT_GUIDE.md` for instructions on deploying this architecture to AWS or GCP.
*   **Data Quality:** Integrate Great Expectations as a dedicated Airflow task.
*   **Real-time Streaming:** Replace `yfinance` with a Kafka producer/consumer setup to simulate true real-time data ingestion.
