# utils/mongo_utils.py
import pymongo
import os

DEFAULT_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")

class MongoConnector:
    def __init__(self, uri=DEFAULT_URI):
        self.uri = uri
        self.client = None

    def __enter__(self):
        self.client = pymongo.MongoClient(self.uri)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()


def get_collection_data(db_name, collection_name, filter_query=None):
    filter_query = filter_query or {}
    with MongoConnector() as client:
        db = client[db_name]
        collection = db[collection_name]
        return list(collection.find(filter_query))


def replace_one_document(db_name, collection_name, filter_query, new_doc):
    with MongoConnector() as client:
        db = client[db_name]
        collection = db[collection_name]
        return collection.replace_one(filter_query, new_doc, upsert=True)


def insert_one_document(db_name, collection_name, doc):
    with MongoConnector() as client:
        db = client[db_name]
        collection = db[collection_name]
        return collection.insert_one(doc)


def insert_many_documents(db_name, collection_name, docs):
    with MongoConnector() as client:
        db = client[db_name]
        collection = db[collection_name]
        return collection.insert_many(docs)


def clear_collection(db_name, collection_name):
    with MongoConnector() as client:
        db = client[db_name]
        collection = db[collection_name]
        collection.delete_many({})
