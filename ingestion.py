import requests
import os
import zipfile
import glob


URL = "https://download.inep.gov.br/microdados/microdados_educacao_superior_2019.zip"

def download_file(url:str):
    local_filename = url.split('/')[-1]
    os.makedirs("temp", exist_ok=True)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"temp/{local_filename}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return

def unzip_files(file_name):
    with zipfile.ZipFile(f"temp/{file_name}", 'r') as zip_ref:
        zip_ref.extractall("temp")
    

if __name__ == "__main__":
    local_filename = URL.split('/')[-1]
    # download_file(url=URL)
    # unzip_files(local_filename)
    print(glob.glob("temp/Microdados_Educaç╞o_Superior_2019/dados/*.CSV"))
