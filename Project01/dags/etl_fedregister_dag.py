from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingestion.ingestion_fedregister import ingest_fedregister
from transform.transform_fedregister import transform_fedregister
from loadmongo import load_to_mongo

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    dag_id='etl_fedregister_dag',
    default_args=default_args,
    description='ETL pipeline for Federal Register API',
    schedule_interval='@daily',
    catchup=False,
    tags=['fedregister', 'ETL']
)

with dag:
    ingest = PythonOperator(
        task_id='ingest_fedregister',
        python_callable=ingest_fedregister
    )

    transform = PythonOperator(
        task_id='transform_fedregister',
        python_callable=transform_fedregister
    )

    load = PythonOperator(
        task_id='load_fedregister',
        python_callable=lambda: load_to_mongo("transformed_fedregister.json", "fedregister")
    )

    ingest >> transform >> load
