FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Copiar solo requirements primero (optimiza cache)
COPY requirements.txt .
# Instalar dependencias del sistema

RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y libpq-dev gcc && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el resto del código de la app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]