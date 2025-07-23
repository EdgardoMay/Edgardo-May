from datetime import datetime

def transform_federal_register_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids="extract_and_load_raw_federal_register_data", key="return_value")

    processed = []
    for doc in raw_data:
        entry = {
            "title": doc.get("title"),
            "document_number": doc.get("document_number"),
            "publication_date": doc.get("publication_date"),
            "type": doc.get("type"),
            "agencies": doc.get("agencies", []),
            "topics": doc.get("topics", []),
            "is_regulatory": doc.get("type") == "Rule",
            "transformation_timestamp": datetime.now().isoformat()
        }
        processed.append(entry)
    
    ti.xcom_push(key="processed_federal_register_data_for_load", value=processed)
    return processed