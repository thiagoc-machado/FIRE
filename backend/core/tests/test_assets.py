import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Category

@pytest.mark.django_db
def test_create_and_list_asset():
    user = get_user_model().objects.create_user(username='teste', password='senha1234')
    client = APIClient()
    client.force_authenticate(user=user)

    categoria = Category.objects.create(nome='Ações')

    payload = {
        'codigo': 'PETR4',
        'nome': 'Petrobras',
        'categoria': categoria.id,
        'moeda': 'BRL',
        'frequencia_dividendos': 'mensal'
    }

    response = client.post('/api/assets/', payload)
    assert response.status_code == 201
    assert response.data['nome'] == 'Petrobras'

    list_response = client.get('/api/assets/')
    assert list_response.status_code == 200
    assert any(asset['codigo'] == 'PETR4' for asset in list_response.data)

