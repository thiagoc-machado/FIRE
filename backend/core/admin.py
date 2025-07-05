from django.contrib import admin
from .models import Category, Broker, Asset, Operation
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'nome', 'categoria', 'moeda', 'frequencia_dividendos']
    list_filter = ['categoria', 'moeda']
    search_fields = ['codigo', 'nome']

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tipo', 'ativo', 'quantidade', 'valor_compra', 'dividendos', 'data']
    list_filter = ['tipo', 'corretora', 'categoria']
    search_fields = ['ativo__codigo', 'user__email']

from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, ClockedSchedule, SolarSchedule

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)
# admin.site.register(CrontabSchedule)
# admin.site.register(ClockedSchedule)
# admin.site.register(SolarSchedule)
