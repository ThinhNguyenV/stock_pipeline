import os
import sys
import time
from datetime import datetime

# Add the src directory to the path to allow module imports
sys.path.append(os.path.dirname(__file__))

from db_init import initialize_database
from data_generator import main as generate_data
from ingestion_script import ingest_data
from transformation_script import main as transform_data

def run_pipeline():
    """
    The main orchestration function for the E-commerce Data Pipeline.
    It executes the steps in the correct order:
    1. Initialize Database Schema
    2. Generate Raw Data
    3. Ingest Raw Data to Staging
    4. Transform and Load Data to Data Warehouse
    """
    
    start_time = time.time()
    print("="*50)
    print(f"E-COMMERCE DATA PIPELINE STARTING at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    # --- Step 1: Initialize Database ---
    print("\n--- STEP 1: INITIALIZING DATABASE ---")
    try:
        initialize_database()
    except Exception as e:
        print(f"FATAL ERROR in DB Initialization: {e}")
        return

    # --- Step 2: Generate Raw Data ---
    print("\n--- STEP 2: GENERATING RAW DATA ---")
    try:
        raw_file_path = generate_data()
        if not raw_file_path:
            print("FATAL ERROR: Data generation failed to return a file path.")
            return
    except Exception as e:
        print(f"FATAL ERROR in Data Generation: {e}")
        return

    # --- Step 3: Ingest Raw Data ---
    print("\n--- STEP 3: INGESTING RAW DATA ---")
    try:
        ingested_count = ingest_data(raw_file_path)
        if ingested_count == 0:
            print("WARNING: No data ingested. Transformation step may be skipped.")
    except Exception as e:
        print(f"FATAL ERROR in Data Ingestion: {e}")
        return

    # --- Step 4: Transform and Load ---
    print("\n--- STEP 4: TRANSFORMING AND LOADING DATA ---")
    try:
        transform_data()
    except Exception as e:
        print(f"FATAL ERROR in Data Transformation: {e}")
        return

    end_time = time.time()
    duration = end_time - start_time
    
    print("="*50)
    print(f"PIPELINE COMPLETED SUCCESSFULLY in {duration:.2f} seconds.")
    print("="*50)

if __name__ == "__main__":
    # Ensure I are in the correct directory to run the script
    # The script is in junior_de_project/src, so I change to junior_de_project
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    
    # Activate the virtual environment for execution
    # In a real-world scenario, the orchestrator (e.g., Airflow) handles the environment.
    # Here, I assume the user has activated the environment manually or I run it directly.
    
    run_pipeline()
