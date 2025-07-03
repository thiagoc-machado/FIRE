import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    register_url = reverse('register')
    login_url = reverse('token_obtain_pair')

    payload = {
        'username': 'thiago',
        'email': 'thiago@example.com',
        'password': 'fire12345'
    }

    response = client.post(register_url, payload)
    assert response.status_code == 201
    assert User.objects.count() == 1

    response = client.post(login_url, {
        'email': payload['email'],
        'password': payload['password']
    })
    assert response.status_code == 200
    assert 'access' in response.data
