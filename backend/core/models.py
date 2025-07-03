from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Broker(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Asset(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    moeda = models.CharField(max_length=10, default='EUR')  # EUR, USD, BRL, etc.
    frequencia_dividendos = models.CharField(max_length=20, default='trimestral')

    def __str__(self):
        return f'{self.codigo}'

class Operation(models.Model):
    TIPO = (('COMPRA', 'Compra'), ('VENDA', 'Venda'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO)
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    corretora = models.ForeignKey(Broker, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    data = models.DateField()
    quantidade = models.DecimalField(max_digits=12, decimal_places=2)
    valor_compra = models.DecimalField(max_digits=12, decimal_places=2)
    dividendos = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-data']
