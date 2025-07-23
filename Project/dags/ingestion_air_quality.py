import requests
from pymongo import MongoClient

def extract_and_load_raw_air_quality_data(**context):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=52.52&longitude=13.41&"
        "hourly=temperature_2m,precipitation_probability,temperature_80m"
    )
    
    client = None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        client = MongoClient("mongo", 27017)
        db = client["etl_project"]
        collection = db["raw_air_quality"]  # Puedes cambiar el nombre si lo prefieres
        collection.insert_one(data)

        print("[INFO] Weather data successfully loaded to MongoDB (raw_air_quality).")

    except requests.exceptions.RequestException as req_err:
        print(f"[ERROR] API request failed: {req_err}")
        raise
    except Exception as e:
        print(f"[ERROR] General failure during ingestion: {e}")
        raise
    finally:
        if client:
            client.close()
