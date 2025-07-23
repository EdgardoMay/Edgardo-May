import json
from pymongo import MongoClient

def load_to_mongo(data, collection_name):
    """
    Carga los datos transformados a MongoDB en la colección especificada.

    Args:
        data (dict or list): Datos transformados.
        collection_name (str): Nombre de la colección donde se insertarán los datos.
    """
    try:
        client = MongoClient("mongodb://mongodb:27017/")
        db = client["etl_database"]

        if isinstance(data, list):
            db[collection_name].insert_many(data)
        else:
            db[collection_name].insert_one(data)

        print(f"✔️  Datos cargados en la colección '{collection_name}'")
    except Exception as e:
        print(f"❌ Error cargando en MongoDB: {e}")
    finally:
        client.close()
