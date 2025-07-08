#!/bin/bash

# Mostra mensagens informativas
echo "🏁 Iniciando entrypoint.sh"

# Espera alguns segundos para garantir que o banco esteja pronto
echo "⏳ Aguardando banco de dados..."
sleep 5

# Executa as migrações
echo "🔄 Rodando migrações..."
python manage.py migrate --noinput

# Coleta arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Inicia o Gunicorn
echo "🚀 Iniciando o servidor Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
