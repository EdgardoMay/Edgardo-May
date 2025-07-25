# 🌎 ETL Pipeline con Airflow, MongoDB y Streamlit

Este proyecto implementa un pipeline ETL completo, construido para la asignatura de **Gestión Masiva de Datos** de la Universidad Politécnica de Yucatán. Se utilizan tres APIs públicas que proporcionan datos del clima, noticias y documentos legales. El flujo se orquesta con Apache Airflow, se almacena en MongoDB y se visualiza a través de un dashboard interactivo con Streamlit.

---

## 🎯 Objetivo

Diseñar un sistema ETL batch que integre múltiples fuentes de datos públicas mediante técnicas de extracción, transformación y carga, todo orquestado con Airflow, almacenado en MongoDB y visualizado gráficamente en tiempo real con Streamlit.

---

## 🧰 Tecnologías Utilizadas

| Componente      | Tecnología       | Puerto | Descripción                                              |
|-----------------|------------------|--------|----------------------------------------------------------|
| Orquestador     | Apache Airflow   | 8080   | Orquesta tareas ETL y visualiza DAGs                    |
| Base de datos   | PostgreSQL       | N/A    | Almacén de metadatos de Airflow                         |
| Almacenamiento  | MongoDB          | 27017  | Guarda datos crudos y transformados                     |
| Dashboard       | Streamlit        | 8501   | Interfaz web para visualizar los datos procesados       |

---

## 🌐 APIs Involucradas

1. **Open-Meteo API (Clima)**
   - Datos horarios: temperatura a distintas alturas, probabilidad de precipitación.
   - Requiere ubicación (lat/lon). Sin autenticación.

2. **Federal Register API**
   - Documentos oficiales publicados por el gobierno de EE.UU.
   - Permite filtros por tipo y fecha. No requiere API key.

3. **NewsAPI**
   - Titulares recientes de noticias. Requiere API Key gratuita.

---

## 📁 Estructura del Proyecto

```plaintext
project/
├── airflow/
│   ├── Dockerfile
│   └── dags/
│       ├── ingestion_air_quality.py
│       ├── ingestion_federal_register.py
│       ├── ingestion_newsapi.py
│       ├── transform_air_quality.py
│       ├── transform_federal_register.py
│       ├── transform_newsapi.py
│       ├── load_mongo.py
│       └── pipeline.py
├── streamlit_app/
│   ├── app.py
│   └── Dockerfile
├── utils/
│   └── mongo_utils.py
├── .env
├── docker-compose.yml
├── requirements.txt
├── setup_pipeline.sh
├── teardown_pipeline.sh
└── README.md
```

---

## 🚀 Ejecución del Proyecto

### Opción A: Usando Script Automatizado

1. **Pre-requisitos**  
   Tener instalado y corriendo Docker Desktop.

2. **Dar permisos de ejecución al script (solo la primera vez):**
```bash
chmod +x setup_pipeline.sh
```

3. **Ejecutar el script:**

- Opción 1:

```bash
./setup_pipeline.sh
```

- Opción 2:

```bash
bash setup_pipeline.sh
```

Este script:
- Inicializa Airflow.
- Crea un usuario administrador.
- Levanta todos los servicios vía `docker-compose`.

4. **Acceder a las interfaces:**
   - Airflow: [http://localhost:8080](http://localhost:8080)
   - Streamlit: [http://localhost:8501](http://localhost:8501)

---

### Opción B: Configuración Manual Paso a Paso

1. **Inicializar la base de datos de Airflow (solo la primera vez):**

```bash
docker compose run airflow-webserver airflow db init
```

2. **Crear usuario administrador en Airflow:**

```bash
docker compose run airflow-webserver airflow users create   --username admin   --firstname Edgardo   --lastname May   --role Admin   --email edgar@example.com   --password airflow
```

3. **Levantar todos los servicios:**

```bash
docker compose up -d --build
```

4. **Verificar que los contenedores estén activos:**

```bash
docker compose ps
```

---

## 📈 Visualización de Datos

1. **Activar el DAG principal:**
   - Ir a [http://localhost:8080](http://localhost:8080)
   - Activar el DAG `main_etl_pipeline`.
   - Ejecutarlo manualmente desde la UI (botón ▶️).

2. **Esperar a que todas las tareas se completen (color verde).**

3. **Ir al dashboard de Streamlit:**
   - [http://localhost:8501](http://localhost:8501)
   - Se mostrarán visualizaciones para:
     - 🌤️ Clima por hora (temperaturas, precipitaciones).
     - 📚 Documentos federales recientes.
     - 🗞️ Noticias recientes por fuente y fecha.

---

## 🧹 Limpieza del Entorno

Para detener y eliminar todos los contenedores y redes:

```bash
docker compose down
```

Para eliminar también los volúmenes (datos de MongoDB y Airflow):

```bash
docker compose down -v
```

---

## ✅ Notas Finales

- Las credenciales de Airflow y las claves API están definidas en el archivo `.env`.
- Puedes modificar los DAGs o agregar nuevos sin reiniciar todos los servicios, solo reiniciar Airflow si agregas nuevos scripts.
- El archivo `teardown_pipeline.sh` elimina el entorno por completo.

---

## 📬 Contacto

Proyecto desarrollado por **Edgardo May** como parte del curso de Ingeniería de Datos, Universidad Politécnica de Yucatán.