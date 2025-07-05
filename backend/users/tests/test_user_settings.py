
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import UserSettings

@pytest.mark.django_db
def test_user_settings_criacao_e_update():
    User = get_user_model()
    user = User.objects.create_user(username='usuario', password='senha123')
    client = APIClient()
    client.force_authenticate(user=user)

    # Acessar configurações (devem ser criadas automaticamente)
    response = client.get('/api/users/settings/')
    assert response.status_code == 200
    assert response.data['moeda_padrao'] == 'EUR'

    # Atualizar configurações
    update_data = {
        'moeda_padrao': 'USD',
        'idioma': 'en',
        'frequencia_atualizacao': 12
    }
    response = client.patch('/api/users/settings/', update_data, format='json')
    assert response.status_code == 200
    assert response.data['moeda_padrao'] == 'USD'

    settings = UserSettings.objects.get(user=user)
    assert settings.idioma == 'en'
    assert settings.frequencia_atualizacao == 12
