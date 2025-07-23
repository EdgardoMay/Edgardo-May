from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime

from ingestion_air_quality import extract_and_load_raw_air_quality_data
from ingestion_federal_register import extract_and_load_raw_federal_register_data
from ingestion_newsapi import extract_and_load_raw_newsapi_data

from transform_air_quality import transform_air_quality_data
from transform_federal_register import transform_federal_register_data
from transform_newsapi import transform_newsapi_data

from load_mongo import load_processed_data_to_mongo

with DAG(
    dag_id='main_etl_pipeline',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['etl', 'multi-api'],
) as dag:

    # Air Quality
    extract_air_quality = PythonOperator(
        task_id='extract_and_load_raw_air_quality_data',
        python_callable=extract_and_load_raw_air_quality_data,
        provide_context=True
    )

    transform_air_quality = PythonOperator(
        task_id='transform_air_quality_data',
        python_callable=transform_air_quality_data,
        provide_context=True
    )

    load_air_quality = PythonOperator(
        task_id='load_processed_air_quality_data',
        python_callable=load_processed_data_to_mongo,
        op_kwargs={
            'collection_name': 'processed_air_quality',
            'xcom_key': 'processed_air_quality_data_for_load',
            'xcom_task_id': 'transform_air_quality_data'
        },
        provide_context=True
    )

    # Federal Register
    extract_federal_register = PythonOperator(
        task_id='extract_and_load_raw_federal_register_data',
        python_callable=extract_and_load_raw_federal_register_data,
        provide_context=True
    )

    transform_federal_register = PythonOperator(
        task_id='transform_federal_register_data',
        python_callable=transform_federal_register_data,
        provide_context=True
    )

    load_federal_register = PythonOperator(
        task_id='load_processed_federal_register_data',
        python_callable=load_processed_data_to_mongo,
        op_kwargs={
            'collection_name': 'processed_federal_register',
            'xcom_key': 'processed_federal_register_data_for_load',
            'xcom_task_id': 'transform_federal_register_data'
        },
        provide_context=True
    )

    # NewsAPI
    extract_newsapi = PythonOperator(
        task_id='extract_and_load_raw_newsapi_data',
        python_callable=extract_and_load_raw_newsapi_data,
        provide_context=True
    )

    transform_newsapi = PythonOperator(
        task_id='transform_newsapi_data',
        python_callable=transform_newsapi_data,
        provide_context=True
    )

    load_newsapi = PythonOperator(
        task_id='load_processed_newsapi_data',
        python_callable=load_processed_data_to_mongo,
        op_kwargs={
            'collection_name': 'processed_newsapi',
            'xcom_key': 'processed_newsapi_data_for_load',
            'xcom_task_id': 'transform_newsapi_data'
        },
        provide_context=True
    )

    # Set dependencies
    extract_air_quality >> transform_air_quality >> load_air_quality
    extract_federal_register >> transform_federal_register >> load_federal_register
    extract_newsapi >> transform_newsapi >> load_newsapi
