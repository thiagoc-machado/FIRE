
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Category, Broker, Asset, Operation
import io

@pytest.mark.django_db
def test_importar_e_exportar_operacoes():
    User = get_user_model()
    user = User.objects.create_user(username='teste', password='senha123')
    client = APIClient()
    client.force_authenticate(user=user)

    categoria = Category.objects.create(nome='Tecnologia')
    corretora = Broker.objects.create(nome='Clear')
    ativo = Asset.objects.create(codigo='AAPL', nome='Apple', categoria=categoria, moeda='USD')

    # Conteúdo do CSV (1 operação)
    csv_content = (
        'tipo,ativo,quantidade,valor_compra,data,dividendos,categoria,corretora\n'
        f'COMPRA,{ativo.id},10,150.0,2024-01-01,2.5,{categoria.id},{corretora.id}\n'
    )
    csv_file = io.BytesIO(csv_content.encode('utf-8'))
    csv_file.name = 'operacoes.csv'

    response = client.post('/api/core/operation/importar/', {'file': csv_file}, format='multipart')
    assert response.status_code == 201
    assert 'importadas' in response.data['mensagem']

    # Verificar se a operação foi criada
    operacoes = Operation.objects.filter(user=user)
    assert operacoes.count() == 1
    assert operacoes.first().quantidade == 10

    # Testar exportação
    response = client.get('/api/core/operation/exportar/')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert response.data[0]['tipo'] == 'COMPRA'
