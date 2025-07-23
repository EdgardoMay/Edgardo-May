from datetime import datetime

def transform_newsapi_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids="extract_and_load_raw_newsapi_data", key="return_value")

    processed = []
    for article in raw_data:
        entry = {
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "author": article.get("author"),
            "description": article.get("description"),
            "url": article.get("url"),
            "is_breaking_news": "breaking" in (article.get("title") or "").lower(),
            "has_media": article.get("urlToImage") is not None,
            "transformation_timestamp": datetime.now().isoformat()
        }
        processed.append(entry)

    # Empujar explícitamente a XCom con la clave esperada
    ti.xcom_push(key="processed_newsapi_data_for_load", value=processed)
    return processed
