# Dockerfile para streamlit_app
FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY ../requirements.txt ./requirements.txt

# ✅ Usa requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
