from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


with DAG(
    'smoke_detection_training',
    default_args={'retries': 2,'retry_delay': timedelta(minutes=5)},
    
    # [END default_args]
    description='Sensor Fault Detection',
    schedule_interval="@hourly",
    start_date=pendulum.datetime(2023, 12, 27, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    
    def training(**kwargs):
        from smoke.pipeline.training_pipeline import start_training_pipeline
        start_training_pipeline()
    
    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

    training_pipeline  = PythonOperator(
            task_id="train_pipeline",
            python_callable=training

    )

    sync_data_to_s3 = PythonOperator(
            task_id="sync_data_to_s3",
            python_callable=sync_artifact_to_s3_bucket

    )

    training_pipeline >> sync_data_to_s3

