import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from core.models import Category, Broker, Asset

@pytest.mark.django_db
def test_create_operation():
    user = User.objects.create_user(username='thiago', email='thiago@example.com', password='fire123')
    client = APIClient()
    client.force_authenticate(user=user)

    category = Category.objects.create(nome='Tecnologia')
    broker = Broker.objects.create(nome='Clear')
    asset = Asset.objects.create(codigo='AAPL', nome='Apple Inc.', categoria=category, moeda='USD')

    payload = {
        'tipo': 'COMPRA',
        'ativo': asset.id,
        'quantidade': 10,
        'valor_compra': 150,
        'data': '2024-01-01',
        'dividendos': 5,
        'categoria': category.id,
        'corretora': broker.id,
    }

    response = client.post(reverse('operation-list'), payload)
    assert response.status_code == 201
    assert float(response.data['quantidade']) == 10.0
