import streamlit as st
import pymongo
import pandas as pd
from datetime import datetime
import plotly.express as px

MONGO_URI = "mongodb://mongo:27017/"

DB_MAP = {
    "air_quality": ("environment_data", "processed_air_quality"),
    "federal_register": ("legal_documents", "processed_federal_register"),
    "newsapi": ("news_data", "processed_newsapi"),
}

@st.cache_data(ttl=600)
def fetch_collection(db_name, collection_name):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[db_name]
        data = list(db[collection_name].find({}))
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error connecting to {db_name}.{collection_name}: {e}")
        return pd.DataFrame()
    finally:
        client.close()

st.set_page_config(page_title="ETL Dashboard", layout="wide")
st.title("📊 ETL Project Dashboard - Clima, Federal Register y Noticias")
st.write("Este dashboard visualiza los datos procesados desde MongoDB después del pipeline ETL.")
st.write("---")

# 🌤️ Datos Meteorológicos
df_air = fetch_collection(*DB_MAP["air_quality"])
if not df_air.empty and "timestamp" in df_air.columns:
    st.subheader("🌤️ Datos Meteorológicos por Hora")

    df_air["timestamp"] = pd.to_datetime(df_air["timestamp"], errors='coerce')
    df_air = df_air.dropna(subset=["timestamp"])
    df_air["hora"] = df_air["timestamp"].dt.strftime('%Y-%m-%d %H:%M')

    st.metric("🔁 Registros procesados", len(df_air))

    fig_temp = px.line(df_air, x="hora", y=["temperature_2m", "temperature_80m"],
                       title="Temperatura a 2m y 80m por hora",
                       labels={"value": "Temperatura (°C)", "hora": "Hora", "variable": "Altura"})
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_precip = px.bar(df_air, x="hora", y="precipitation_probability",
                        title="Probabilidad de precipitación por hora",
                        labels={"hora": "Hora", "precipitation_probability": "% Precipitación"})
    st.plotly_chart(fig_precip, use_container_width=True)
else:
    st.info("No hay datos de clima disponibles.")
st.write("---")

# 📚 Federal Register
df_fed = fetch_collection(*DB_MAP["federal_register"])
if not df_fed.empty and "publication_date" in df_fed.columns:
    st.subheader("📚 Documentos del Federal Register")

    df_fed["publication_date"] = pd.to_datetime(df_fed["publication_date"], errors='coerce')
    df_fed = df_fed.dropna(subset=["publication_date"])

    min_date = df_fed["publication_date"].min().date()
    max_date = df_fed["publication_date"].max().date()

    selected_range = st.date_input("Filtrar por rango de fechas:", [min_date, max_date])

    if len(selected_range) == 2:
        start_date, end_date = selected_range
        df_fed = df_fed[(df_fed["publication_date"] >= pd.to_datetime(start_date)) &
                        (df_fed["publication_date"] <= pd.to_datetime(end_date))]

    st.metric("📄 Documentos disponibles", len(df_fed))

    latest = df_fed.sort_values("publication_date", ascending=False).head(5)
    st.write(latest[["title", "publication_date", "type"]])

    if "type" in df_fed.columns:
        fig_types = px.pie(df_fed, names="type", title="Distribución de tipos de documentos federales")
        st.plotly_chart(fig_types, use_container_width=True)
else:
    st.info("No hay documentos del Federal Register disponibles.")
st.write("---")

# 🗞️ Noticias
df_news = fetch_collection(*DB_MAP["newsapi"])
if not df_news.empty and "published_at" in df_news.columns:
    st.subheader("🗞️ Noticias Recientes")

    df_news["published_at"] = pd.to_datetime(df_news["published_at"], errors='coerce')
    df_news = df_news.dropna(subset=["published_at"])

    if "source" not in df_news.columns:
        df_news["source"] = "Desconocido"

    sources = sorted(df_news["source"].dropna().unique())
    selected_sources = st.multiselect("Filtrar por fuente de noticias:", options=sources, default=sources)
    df_news_filtered = df_news[df_news["source"].isin(selected_sources)]

    st.metric("📰 Artículos de noticias", len(df_news_filtered))

    st.write(df_news_filtered[["title", "source", "published_at"]].head(10))

    source_counts = df_news_filtered["source"].value_counts().reset_index()
    source_counts.columns = ["source", "count"]

    fig_sources = px.bar(
        source_counts,
        x="source", y="count",
        title="Número de noticias por fuente",
        labels={"source": "Fuente", "count": "Cantidad"}
    )
    st.plotly_chart(fig_sources, use_container_width=True)

    df_news_filtered["date"] = df_news_filtered["published_at"].dt.date
    daily_counts = df_news_filtered.groupby("date").size().reset_index(name="count")
    fig_time = px.line(daily_counts, x="date", y="count",
                       title="Artículos publicados por día",
                       labels={"date": "Fecha", "count": "Cantidad"})
    st.plotly_chart(fig_time, use_container_width=True)
else:
    st.info("No hay artículos de noticias disponibles.")
st.write("---")


