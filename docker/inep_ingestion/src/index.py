from datetime import datetime
import boto3
from pathlib import Path
import requests
import os
import shutil
import zipfile
from clint.textui import progress

INEP_2019_URL = os.getenv("inep_2019_url", "https://download.inep.gov.br/microdados/microdados_educacao_superior_2019.zip")
AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")
LANDING_ZONE = os.getenv("landing_zone")

class IngestionINEP:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.url = INEP_2019_URL

    def donwload_file(self) -> str:
        filename = self.url.split('/')[-1]
        path = Path.joinpath(Path.cwd(), "temp", filename)
        print("Downloading file")
        r = requests.get(self.url, stream=True)
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return path
    
    def unzip_file(self, zip_file_path:str) -> list:
        print("Unziping...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            folder = Path(zip_file_path).parent.absolute()
            files = zip_ref.namelist()
            zip_ref.extractall(folder)
        
        files = [str(Path.joinpath(folder, x)) for x in files]
        return list(filter(lambda x: x.endswith(".CSV"), files))
    
    def upload_files(self, files:list) -> None:
        for file in files:
            filename = file.split("/")[-1]
            folder = filename.replace("_2019.CSV", "")
            self.s3_client.upload_file(
                file, LANDING_ZONE, f"inep/{folder}/ano=2019/{filename}"
            )
    

        
if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    try:
        inep = IngestionINEP()
        file = inep.donwload_file()
        files = inep.unzip_file(file)
        inep.upload_files(files)
    except Exception as e:
        shutil.rmtree("temp")
        raise Exception(e)
    shutil.rmtree("temp")
    