import requests
import pymongo
from datetime import datetime

def extract_and_load_raw_federal_register_data(**kwargs):
    ti = kwargs['ti']
    URL = "https://www.federalregister.gov/api/v1/documents.json"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        raw_data = response.json()

        client = pymongo.MongoClient("mongodb://mongo:27017/")
        db = client["legal_documents"]
        collection = db["raw_federal_register"]
        collection.delete_many({})
        raw_data['ingestion_timestamp'] = datetime.now().isoformat()
        collection.insert_one(raw_data)
        ti.xcom_push(key="raw_federal_register_data_for_transform", value=raw_data['results'])
        return raw_data['results']
    finally:
        client.close()
