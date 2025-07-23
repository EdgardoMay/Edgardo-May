from datetime import datetime

def transform_air_quality_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids="extract_and_load_raw_air_quality_data", key="return_value")

    if not raw_data or "hourly" not in raw_data:
        print("[WARNING] No hourly data found in raw weather data.")
        ti.xcom_push(key="processed_air_quality_data_for_load", value=[])
        return []

    hourly_data = raw_data["hourly"]
    times = hourly_data.get("time", [])
    temps_2m = hourly_data.get("temperature_2m", [])
    temps_80m = hourly_data.get("temperature_80m", [])
    precipitation_probs = hourly_data.get("precipitation_probability", [])

    processed = []
    for i in range(len(times)):
        record = {
            "timestamp": times[i],
            "temperature_2m": temps_2m[i] if i < len(temps_2m) else None,
            "temperature_80m": temps_80m[i] if i < len(temps_80m) else None,
            "precipitation_probability": precipitation_probs[i] if i < len(precipitation_probs) else None,
            "transformation_timestamp": datetime.now().isoformat()
        }
        processed.append(record)

    # Push to XCom for loading
    ti.xcom_push(key="processed_air_quality_data_for_load", value=processed)
    return processed
