FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho que será montado pelo volume
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    postgresql-client \
    && pip install --upgrade pip \
    && pip install watchdog \
    && rm -rf /var/lib/apt/lists/*

# Instala apenas requirements (o código será mapeado pelo volume)
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]