from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    moeda_padrao = models.CharField(max_length=5, default='EUR')  # Ex: EUR, USD, BRL
    idioma = models.CharField(max_length=10, default='pt')  # Ex: pt, en, es
    frequencia_atualizacao = models.PositiveIntegerField(default=24)  # em horas

    meta_fire_total = models.DecimalField(max_digits=12, decimal_places=2, default=600000)
    renda_fire_desejada = models.DecimalField(max_digits=10, decimal_places=2, default=2000)

    def __str__(self):
        return f'Settings de {self.user.username}'
