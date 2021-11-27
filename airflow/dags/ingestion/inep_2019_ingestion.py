from airflow import DAG
from airflow.models import Variable

# Operators
from airflow.operators.python import PythonOperator


from datetime import datetime
import boto3
import requests
import os
import shutil
import zipfile
import glob

INEP_2019_URL = Variable.get("inep_2019_url")
AWS_ACCESS_KEY_ID = Variable.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = Variable.get("aws_secret_access_key")
LANDING_ZONE = Variable.get("landing_zone")

default_args = {
    'owner': 'Igor Magro',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}


def fn_download_and_unzip():
    def download_file(url:str) -> str:
        local_filename = url.split('/')[-1]

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"temp/{local_filename}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return local_filename

    def unzip_files(file_name: str) -> list:
        with zipfile.ZipFile(f"temp/{file_name}", 'r') as zip_ref:
            zip_ref.extractall("temp")

        return glob.glob("temp/Microdados_Educaç╞o_Superior_2019/dados/*.CSV")
    
    os.makedirs("temp", exist_ok=True)
    file_name = download_file(url=INEP_2019_URL)
    data_files = unzip_files(file_name=file_name)

    return data_files

def fn_upload_to_s3(ti) -> None:
    get_xcom_file_name = ti.xcom_pull(task_ids=['download_and_unzip_files'])

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    for file_path in get_xcom_file_name[0]:
        file_name = file_path.split('/')[-1]
        folder_name = file_name.replace("_2019.CSV", "")
        s3_client.upload_file(file_path, LANDING_ZONE, f"inep/{folder_name.lower()}/ano=2019/{file_name}")

    shutil.rmtree("temp", ignore_errors=True)
    return
    


with DAG(
    'inep_2019_ingestion',
    start_date=datetime(2019, 1, 1),
    max_active_runs=16,
    schedule_interval= None,  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False, # enable if you don't want historical dag runs to run
    tags=["inep","python","ingestion"]
) as dag:

   download_and_unzip_file = PythonOperator(
       task_id="download_and_unzip_files",
       python_callable=fn_download_and_unzip
   )

   upload_files_to_datalake = PythonOperator(
       task_id="upload_files_to_datalake",
       python_callable=fn_upload_to_s3
   )

download_and_unzip_file >> upload_files_to_datalake

