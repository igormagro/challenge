from airflow import DAG
from airflow.models import Variable

# Airflow Operators
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

# Airflow Sensors
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

import boto3

from datetime import datetime, timedelta

INEP_2019_URL = Variable.get("inep_2019_url")
aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")
raw_zone = Variable.get("raw_zone")

default_args = {
    'owner': 'Igor Magro',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG(
    'inep_2019_ingestion',
    start_date=datetime(2018, 1, 1),
    max_active_runs=16,
    schedule_interval= None,  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False, # enable if you don't want historical dag runs to run
    tags=["INEP","Ingestion","CSV"]
) as dag:

    donwload_and_ingest = KubernetesPodOperator(
        task_id="donwload_and_ingest",
        namespace="airflow",
        image=Variable.get("python_container_image"),
        arguments=[f"/opt/app/index.py"],
        env_vars={
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "landing_zone": raw_zone,
        },
        image_pull_policy="Always",
        name="donwload_and_ingest",
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True
    ) 

    verify_file_existence_raw_zone = S3KeySensor(
        task_id='verify_file_existence_raw_zone',
        bucket_name=raw_zone,
        bucket_key='inep/*.CSV',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='aws_default',
    )

donwload_and_ingest >> verify_file_existence_raw_zone