"""
Transform module for Air Quality data.

This script processes raw data from the Open AQ API and prepares it
for loading into MongoDB. It standardizes structure and extracts
relevant metrics.

Author: Edgardo M.M.G.
Date: 2025-07-22
"""

from datetime import datetime


def transform_air_quality(data):
    """
    Transforms raw air quality API response into a clean format.

    Args:
        data (dict): Raw JSON response from the Open AQ API.

    Returns:
        list: List of transformed air quality records.
    """

    if not isinstance(data, dict):
        raise ValueError("Expected a dictionary from the API response.")

    results = data.get("results", [])
    if not results:
        return []

    transformed = []
    for record in results:
        transformed_record = {
            "location": record.get("location"),
            "city": record.get("city"),
            "country": record.get("country"),
            "parameter": record.get("parameter"),
            "value": record.get("value"),
            "unit": record.get("unit"),
            "coordinates": record.get("coordinates"),
            "date_utc": record.get("date", {}).get("utc"),
            "date_local": record.get("date", {}).get("local"),
            "ingested_at": datetime.utcnow().isoformat()
        }
        transformed.append(transformed_record)

    return transformed
