# backend/config/celery.py
import os
from celery import Celery

# Define a variável de ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Cria a instância da aplicação Celery
app = Celery('fire')

# Carrega configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover de tarefas nos apps Django
app.autodiscover_tasks()
