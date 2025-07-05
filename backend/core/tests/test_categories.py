import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Category

@pytest.mark.django_db
def test_crud_category():
    user = get_user_model().objects.create_user(username='usercat', password='senha123')
    client = APIClient()
    client.force_authenticate(user=user)

    # Create
    response = client.post('/api/core/category/', {'nome': 'Tecnologia'})
    assert response.status_code == 201
    category_id = response.data['id']

    # List
    response = client.get('/api/core/category/')
    assert response.status_code == 200
    assert any(cat['nome'] == 'Tecnologia' for cat in response.data)

    # Update
    response = client.put(f'/api/core/category/{category_id}/', {'nome': 'Tech'})
    assert response.status_code == 200
    assert response.data['nome'] == 'Tech'

    # Delete
    response = client.delete(f'/api/core/category/{category_id}/')
    assert response.status_code == 204
    assert not Category.objects.filter(id=category_id).exists()
