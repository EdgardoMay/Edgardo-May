#!/bin/bash

echo "🧹 Deteniendo y limpiando contenedores previos..."
docker compose down --volumes --remove-orphans
rm -f airflow.db airflow-webserver.pid

echo "📦 Inicializando base de datos de Airflow..."
docker compose up -d mongodb
sleep 5

docker compose run --rm airflow airflow db init

echo "👤 Creando usuario administrador: airflow..."
docker compose run --rm airflow airflow users create \
    --username airflow \
    --firstname Air \
    --lastname Flow \
    --role Admin \
    --email airflow@example.com \
    --password airflow

echo "🚀 Levantando todos los servicios..."
docker compose up -d --build

echo "⏳ Esperando a que los servicios arranquen..."
sleep 10

echo "📋 Estado actual de los servicios:"
docker compose ps

echo "✅ Accede a Airflow en: http://localhost:8080"
