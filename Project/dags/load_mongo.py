from airflow.models.dag import DAG
from datetime import datetime
import pymongo
import json
from bson.objectid import ObjectId

MONGO_CONNECTION_STRING = "mongodb://mongo:27017/"

def convert_objectid_to_str(obj):
    if isinstance(obj, dict):
        return {k: convert_objectid_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid_to_str(elem) for elem in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def load_processed_data_to_mongo(**kwargs):
    ti = kwargs['ti']

    collection_name = kwargs.get('collection_name')
    xcom_key = kwargs.get('xcom_key')
    xcom_task_id = kwargs.get('xcom_task_id')

    if not collection_name or not xcom_key or not xcom_task_id:
        raise ValueError("load_processed_data_to_mongo requiere 'collection_name', 'xcom_key' y 'xcom_task_id' en op_kwargs.")

    processed_data = ti.xcom_pull(task_ids=xcom_task_id, key="return_value")

    print(f"DEBUG: Contenido de processed_data recibido para carga en '{collection_name}': {processed_data[:500] if isinstance(processed_data, list) else processed_data}")
    print(f"DEBUG: Tipo de processed_data: {type(processed_data)}")

    if not processed_data:
        print(f"ADVERTENCIA: No hay datos procesados para cargar en '{collection_name}'. Saltando carga.")
        return

    print(f"Iniciando carga de datos procesados en MongoDB en la colección: {collection_name}...")

    client = None
    try:
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)

        if "air_quality" in collection_name:
            db_name = "environment_data"
        elif "federal_register" in collection_name:
            db_name = "legal_documents"
        elif "newsapi" in collection_name:
            db_name = "news_data"
        else:
            raise ValueError(f"Base de datos no definida para la colección: {collection_name}")

        db = client[db_name]
        collection = db[collection_name]

        print(f"Limpiando la colección {collection_name} antes de insertar nuevos datos...")
        collection.delete_many({})
        print("Colección limpiada exitosamente.")

        cleaned_data_for_mongo = convert_objectid_to_str(processed_data)

        # ✅ Validación adicional
        if not isinstance(cleaned_data_for_mongo, list) or not all(isinstance(doc, dict) for doc in cleaned_data_for_mongo):
            raise ValueError(f"Los datos transformados para {collection_name} no son una lista de diccionarios válida.")

        collection.insert_many(cleaned_data_for_mongo)

        print(f"Datos cargados exitosamente en MongoDB en {db_name}.{collection_name}.")
        print(f"Registros cargados (procesados): {len(cleaned_data_for_mongo)} en {collection_name}")

    except pymongo.errors.ConnectionFailure as e:
        print(f"Error de conexión a MongoDB durante la carga en '{collection_name}': {e}")
        raise
    except Exception as e:
        print(f"Error inesperado durante la carga en '{collection_name}': {e}")
        raise
    finally:
        if client:
            client.close()
