#!/bin/bash

# Espera pelo banco
echo "Aguardando o banco de dados iniciar..."
sleep 5

# Roda migrations e coleta arquivos estáticos
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Inicia o Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
