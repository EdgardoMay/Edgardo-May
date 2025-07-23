import requests
import json

def ingest_data(**kwargs):
    url = "https://api.openaq.org/v2/latest"
    response = requests.get(url)
    data = response.json()

    # Guardar el archivo JSON como respaldo
    with open("/app/data/airquality_raw.json", "w") as f:
        json.dump(data, f)

    # Pasar los datos crudos al siguiente paso del DAG
    kwargs['ti'].xcom_push(key='raw_data', value=data)
