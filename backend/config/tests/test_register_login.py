import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    register_data = {
        'username': 'teste',
        'email': 'teste@example.com',
        'password': 'senha1234'
    }
    response = client.post('/api/auth/users/', register_data)
    assert response.status_code == 201

    login_data = {
        'username': 'teste',
        'password': 'senha1234'
    }
    response = client.post('/api/auth/jwt/create/', login_data)
    assert response.status_code == 200
    assert 'access' in response.data
