from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import UserSettings
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemplo de configurações',
            value={
                'moeda_padrao': 'EUR',
                'idioma': 'pt',
                'frequencia_atualizacao': 24
            }
        )
    ]
)
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'moeda_padrao',
            'idioma',
            'frequencia_atualizacao',
            'meta_fire_total',
            'renda_fire_desejada'
        ]

