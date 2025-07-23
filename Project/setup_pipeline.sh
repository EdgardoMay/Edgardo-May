#!/bin/bash

set -e

# 0. Verificar que .env existe
if [ ! -f .env ]; then
  echo "❌ Error: No se encontró el archivo .env en el directorio actual."
  echo "🔧 Crea un archivo .env con las variables necesarias (ej. AIRFLOW__CORE__FERNET_KEY, POSTGRES_USER...)"
  exit 1
fi

echo "🧹 Limpiando entorno previo (por si acaso)..."
docker compose down --volumes --remove-orphans

echo "🚀 Iniciando construcción del entorno ETL..."

# 1. Construir imágenes
echo "🔧 Construyendo imágenes con Docker Compose..."
docker compose build

# 2. Inicializar la base de datos de Airflow
echo "📦 Inicializando la base de datos de Airflow..."
docker compose run --rm airflow-webserver airflow db init

# 3. Crear usuario administrador
echo "👤 Creando usuario administrador: airflow..."
docker compose run --rm airflow-webserver airflow users create \
  --username airflow \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email airflow@upy.mx \
  --password airflow

# 4. Levantar servicios
echo "🚢 Levantando servicios en segundo plano..."
docker compose up -d

# 5. Mensaje final
echo "✅ Entorno ETL listo."
echo "🌐 Accede a Airflow:    http://localhost:8080"
echo "🌐 Accede al dashboard: http://localhost:8501"

