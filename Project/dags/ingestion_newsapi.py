import requests
import pymongo
import os
from dotenv import load_dotenv
from airflow.models import Variable

# Cargar variables de entorno desde .env
load_dotenv()

def extract_and_load_raw_newsapi_data(**kwargs):
    print("Conectando a la API de noticias...")

    client = None
    try:
        # Cargar API Key desde .env
        api_key = os.getenv("GNEWS_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GNEWS_API_KEY en el entorno")

        url = f"https://gnews.io/api/v4/top-headlines?topic=world&lang=en&country=us&max=10&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()

        articles = response.json().get("articles", [])
        print(f"Total de artículos extraídos: {len(articles)}")

        # Guardar en MongoDB
        client = pymongo.MongoClient("mongodb://mongo:27017/")
        db = client["news_data"]
        collection = db["raw_newsapi_data"]
        collection.delete_many({})
        collection.insert_many(articles)

        # Guardar resultado en XCom (solo parte básica, sin ObjectId)
        simplified_articles = [
            {
                "title": a.get("title"),
                "url": a.get("url"),
                "created_utc": None  # Esto se transformará luego
            }
            for a in articles
        ]
        kwargs['ti'].xcom_push(key="return_value", value=simplified_articles)

    except Exception as e:
        print(f"Error en extracción de noticias: {e}")
        raise
    finally:
        if client:
            client.close()
