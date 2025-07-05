import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Broker

@pytest.mark.django_db
def test_crud_broker():
    user = get_user_model().objects.create_user(username='userbroker', password='senha123')
    client = APIClient()
    client.force_authenticate(user=user)

    # Create
    response = client.post('/api/core/broker/', {'nome': 'Clear'})
    assert response.status_code == 201
    broker_id = response.data['id']

    # List
    response = client.get('/api/core/broker/')
    assert response.status_code == 200
    assert any(b['nome'] == 'Clear' for b in response.data)

    # Update
    response = client.put(f'/api/core/broker/{broker_id}/', {'nome': 'XP Investimentos'})
    assert response.status_code == 200
    assert response.data['nome'] == 'XP Investimentos'

    # Delete
    response = client.delete(f'/api/core/broker/{broker_id}/')
    assert response.status_code == 204
    assert not Broker.objects.filter(id=broker_id).exists()
