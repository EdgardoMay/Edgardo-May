# ETL Project

This project performs ETL on data from 3 public APIs: Air Quality, News, and Federal Register.

1. Clone the repository:
   ```bash
   git clone <your_repo>
   cd <your_repo>

2. Build the containers:
    docker-compose up --build

3. Access to Airflow:
    http://localhost:8080
    user: admin
    pass: admin

4. Trigger DAGs:
    etl_airquality_dag
    etl_news_dag
    etl_fedregister_dag

5. Output:
    Cleaned data is loaded into MongoDB
    JSON backup can be dumped with:
        docker exec -it mongodb bash
        mongodump --out /dump



# Proyecto ETL con Apache Airflow y MongoDB

Este proyecto implementa un pipeline ETL (Extracción, Transformación y Carga) para recopilar datos desde tres APIs públicas (calidad del aire, noticias y documentos del Federal Register), procesarlos y almacenarlos en una base de datos MongoDB. El flujo está orquestado mediante Apache Airflow y empaquetado con Docker.

---

## 🚀 Tecnologías utilizadas

- **Apache Airflow 2.8.1** – Orquestación del pipeline
- **MongoDB 6.0** – Almacenamiento NoSQL
- **Python 3.10** – Scripts ETL modulares
- **Docker & Docker Compose** – Contenedores y gestión del entorno

---

## 📁 Estructura del proyecto

```
project-root/
├── dags/                   # DAGs de Airflow (opcional)
├── ingestion/              # Scripts de extracción
├── transform/              # Scripts de transformación
├── mainpipeline.py         # Ejecuta el pipeline completo
├── loadmongo.py            # Carga datos a MongoDB
├── requirements.txt        # Dependencias Python
├── docker-compose.yml      # Orquestación de servicios
├── dockerfile              # Imagen de Airflow personalizada
├── .env                    # Variables de entorno (API keys, URI Mongo, etc.)
├── setup_airflow.sh        # Script automático de instalación y arranque
└── README.md               # Documentación del proyecto
```

---

## ⚙️ Instalación y ejecución rápida

### 1. Clona el repositorio y accede al directorio:
```bash
git clone https://github.com/usuario/proyecto-etl.git
cd proyecto-etl
```

### 2. Configura el archivo `.env`:

```dotenv
MONGO_URI=mongodb://mongodb:27017/
AIRFLOW__CORE__LOAD_EXAMPLES=False
```

### 3. Ejecuta el script automático:
```bash
./setup_airflow.sh
```

Esto hará:
- Inicializar la base de datos de Airflow
- Crear el usuario `airflow` / `airflow`
- Levantar todos los contenedores

### 4. Accede a la interfaz web:

📍 http://localhost:8080  
👤 Usuario: `airflow`  
🔑 Contraseña: `airflow`

---

## 🧪 Ejecución manual del pipeline ETL

Para ejecutar el pipeline completo de forma manual:
```bash
docker compose exec airflow python /app/mainpipeline.py
```

Esto extraerá datos, los transformará, los cargará en MongoDB y generará archivos `.json` de respaldo en tu máquina host.

---

## 📝 Notas importantes

- MongoDB se expone en el puerto `27017`
- Airflow usa SQLite por defecto (persistido en el volumen `airflow_data`)
- Los DAGs pueden ser migrados a Airflow posteriormente, si lo deseas
- Recuerda instalar Docker y Docker Compose antes de iniciar

---

## 👨‍💻 Autor

- **Edgardo May** – Ingeniería en Datos, Proyecto Escolar UPPY


