from __future__ import annotations
import pendulum
import sys
import os
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_utils import initialize_database
from src.extract import fetch_and_load_data, TICKERS
from src.transform import transform_data
from src.load import load_data

with DAG(
    dag_id="stock_price_etl_pipeline",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None, 
    catchup=False,
    tags=["etl", "stock_market"],
    default_args={
        "owner": "airflow",
        "retries": 1,
    }
) as dag:
    
    t1 = PythonOperator(
        task_id="initialize_database",
        python_callable=initialize_database,
    )

    t2 = PythonOperator(
        task_id="extract_raw_data",
        python_callable=fetch_and_load_data,
        op_kwargs={"tickers": TICKERS},
    )

    t3 = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    t4 = PythonOperator(
        task_id="load_analyzed_data",
        python_callable=load_data,
        op_kwargs={"transformed_df": t3.output},
    )

    t1 >> t2 >> t3 >> t4