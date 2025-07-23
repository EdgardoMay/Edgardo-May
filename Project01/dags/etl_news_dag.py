from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingestion.ingestion_news import ingest_news
from transform.transform_news import transform_news
from loadmongo import load_to_mongo

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    dag_id='etl_news_dag',
    default_args=default_args,
    description='ETL pipeline for news API',
    schedule_interval='@daily',
    catchup=False,
    tags=['news', 'ETL']
)

with dag:
    ingest = PythonOperator(
        task_id='ingest_news',
        python_callable=ingest_news
    )

    transform = PythonOperator(
        task_id='transform_news',
        python_callable=transform_news
    )

    load = PythonOperator(
        task_id='load_news',
        python_callable=lambda: load_to_mongo("transformed_news.json", "news")
    )

    ingest >> transform >> load
