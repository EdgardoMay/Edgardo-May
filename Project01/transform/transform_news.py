from datetime import datetime

def transform_news_data(data):
    """
    Transforma los datos de la API de noticias.

    Args:
        data (dict): Objeto JSON crudo de la API de noticias.

    Returns:
        list: Lista de noticias transformadas.
    """
    articles = data.get("articles", [])
    transformed = []

    for article in articles:
        transformed_article = {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "published_at": article.get("publishedAt"),
            "source": article.get("source", {}).get("name"),
            "retrieved_at": datetime.utcnow().isoformat()
        }
        transformed.append(transformed_article)

    return transformed
