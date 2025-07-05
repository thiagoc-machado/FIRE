from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Category, Broker, Asset, Operation


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemplo de categoria',
            value={'id': 1, 'nome': 'Tecnologia'}
        )
    ]
)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemplo de corretora',
            value={'id': 1, 'nome': 'XP Investimentos'}
        )
    ]
)
class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = '__all__'


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemplo de ativo',
            value={
                'id': 1,
                'codigo': 'AAPL',
                'nome': 'Apple Inc.',
                'categoria': 1,
                'moeda': 'USD',
                'frequencia_dividendos': 'trimestral'
            }
        )
    ]
)
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemplo de operação',
            value={
                'id': 1,
                'tipo': 'COMPRA',
                'ativo': 1,
                'quantidade': 10,
                'valor_compra': 150.0,
                'data': '2024-01-01',
                'dividendos': 5.0,
                'categoria': 1,
                'corretora': 1,
                'user': 1
            }
        )
    ]
)
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
        read_only_fields = ['user']
