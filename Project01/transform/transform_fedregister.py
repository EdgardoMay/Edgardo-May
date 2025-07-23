from datetime import datetime

def transform_federal_register_data(data):
    """
    Transforma los datos de la API del Federal Register.

    Args:
        data (dict): Objeto JSON crudo obtenido de la API del Federal Register.

    Returns:
        list: Lista de documentos transformados.
    """
    results = data.get("results", [])
    transformed = []

    for document in results:
        transformed_doc = {
            "title": document.get("title"),
            "document_number": document.get("document_number"),
            "type": document.get("type"),
            "publication_date": document.get("publication_date"),
            "agencies": document.get("agencies", []),
            "html_url": document.get("html_url"),
            "pdf_url": document.get("pdf_url"),
            "abstract": document.get("abstract"),
            "retrieved_at": datetime.utcnow().isoformat()
        }
        transformed.append(transformed_doc)

    return transformed
