import requests
import json
import os

def ingest_data(**kwargs):
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Guardar el archivo JSON como respaldo
    with open("/app/data/news_raw.json", "w") as f:
        json.dump(data, f)

    kwargs['ti'].xcom_push(key='raw_data', value=data)
