# main_pipeline.py
from ingestion_airquality import fetch_air_quality_data
from ingestion_news import fetch_news_data
from ingestion_fedregister import fetch_federal_documents
from transform_airquality import transform_air_quality_data
from transform_news import transform_news_data
from transform_fedregister import transform_federal_data
from loadmongo import load_to_mongo
import os

SAVE_PATH = "/c/Users/edgar/Documents/git_projects"

def save_json_file(data, filename):
    import json
    filepath = os.path.join(SAVE_PATH, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {filepath}")

def run_etl():
    air_data = fetch_air_quality_data()
    news_data = fetch_news_data()
    fed_data = fetch_federal_documents()

    transformed_air = transform_air_quality_data(air_data)
    transformed_news = transform_news_data(news_data)
    transformed_fed = transform_federal_data(fed_data)

    load_to_mongo(transformed_air, "air_quality")
    load_to_mongo(transformed_news, "news_articles")
    load_to_mongo(transformed_fed, "federal_documents")

    save_json_file(transformed_air, "air_quality.json")
    save_json_file(transformed_news, "news_articles.json")
    save_json_file(transformed_fed, "federal_documents.json")

if __name__ == '__main__':
    run_etl()
