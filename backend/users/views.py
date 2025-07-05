from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .models import UserSettings
from .serializers import UserSettingsSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

User = get_user_model()

@extend_schema(
    tags=['Usuários'],
    summary='Registrar novo usuário',
    description='Cria um novo usuário com os dados fornecidos (username, email e senha).',
    examples=[
        OpenApiExample(
            name='Exemplo de registro',
            value={
                'username': 'usuario123',
                'email': 'usuario@example.com',
                'password': 'senhaSegura123'
            },
            request_only=True
        )
    ]
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def criar_settings_usuario(sender, instance, created, **kwargs):
        if created:
            UserSettings.objects.get_or_create(user=instance)


@extend_schema(
    tags=['Configurações'],
    summary='Ver ou atualizar configurações do usuário',
    description='Permite visualizar ou atualizar as preferências de moeda, idioma e frequência de atualização.',
)
class UserSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return settings

