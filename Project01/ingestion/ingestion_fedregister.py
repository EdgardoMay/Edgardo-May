import requests
import json

def ingest_data(**kwargs):
    url = "https://www.federalregister.gov/api/v1/documents.json"
    response = requests.get(url)
    data = response.json()

    with open("/app/data/fedregister_raw.json", "w") as f:
        json.dump(data, f)

    kwargs['ti'].xcom_push(key='raw_data', value=data)
