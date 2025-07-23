from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingestion.ingestion_airquality import ingest_airquality
from transform.transform_airquality import transform_airquality
from loadmongo import load_to_mongo

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    dag_id='etl_airquality_dag',
    default_args=default_args,
    description='ETL pipeline for air quality API',
    schedule_interval='@daily',
    catchup=False,
    tags=['airquality', 'ETL']
)

with dag:
    ingest = PythonOperator(
        task_id='ingest_airquality',
        python_callable=ingest_airquality
    )

    transform = PythonOperator(
        task_id='transform_airquality',
        python_callable=transform_airquality
    )

    load = PythonOperator(
        task_id='load_airquality',
        python_callable=lambda: load_to_mongo("transformed_airquality.json", "airquality")
    )

    ingest >> transform >> load
