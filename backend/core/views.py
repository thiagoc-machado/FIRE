from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .models import Category, Broker, Asset, Operation
from .serializers import CategorySerializer, BrokerSerializer, AssetSerializer, OperationSerializer
from .services.yahoo_service import buscar_dados_ativo


@extend_schema(tags=['Categorias'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Corretoras'])
class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Ativos'])
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Atualizar cotações via Yahoo Finance',
        description='Busca e retorna a cotação atual, moeda, dividend yield e frequência de dividendos para todos os ativos cadastrados, usando a API do Yahoo Finance.',
        responses={
            200: OpenApiResponse(
                description='Lista de ativos com dados atualizados',
                examples=[
                    OpenApiExample(
                        'Exemplo de resposta',
                        value={
                            'ativos_atualizados': [
                                {
                                    'codigo': 'AAPL',
                                    'nome': 'Apple Inc.',
                                    'cotacao': 213.55,
                                    'moeda': 'USD',
                                    'dividend_yield': 0.51,
                                    'frequencia': 1.04
                                }
                            ]
                        },
                        response_only=True
                    )
                ]
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='atualizar')
    def atualizar_cotacoes(self, request):
        atualizados = []
        for asset in self.get_queryset():
            dados = buscar_dados_ativo(asset.codigo)
            if dados['cotacao']:
                atualizados.append({
                    'codigo': asset.codigo,
                    'nome': dados['nome'],
                    'cotacao': dados['cotacao'],
                    'moeda': dados['moeda'],
                    'dividend_yield': dados['dividend_yield'],
                    'frequencia': dados['frequencia'],
                })
        return Response({'ativos_atualizados': atualizados})


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .models import Operation
from .serializers import OperationSerializer


@extend_schema(tags=['Operações'])
class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.none()  # evita erro no router
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)

    @extend_schema(
        summary='Criar operação de compra ou venda',
        examples=[
            OpenApiExample(
                'Exemplo de operação',
                value={
                    'tipo': 'COMPRA',
                    'ativo': 1,
                    'quantidade': 10,
                    'valor_compra': 150.0,
                    'data': '2024-01-01',
                    'dividendos': 5.0,
                    'categoria': 1,
                    'corretora': 1
                },
                request_only=True
            )
        ]
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary='Importar operações via CSV',
        description='Permite importar operações de compra/venda a partir de um arquivo CSV com cabeçalhos: tipo,ativo,quantidade,valor_compra,data,dividendos,categoria,corretora.',
        methods=['POST'],
        request=None,
        responses={201: OpenApiResponse(description='Importação realizada com sucesso')}
    )
    @action(detail=False, methods=['post'], url_path='importar', parser_classes=[MultiPartParser])
    def importar(self, request):
        import csv, io
        file = request.FILES.get('file')
        if not file:
            return Response({'erro': 'Arquivo não enviado'}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        criadas = 0
        for row in reader:
            try:
                data = {
                    'user': request.user.id,
                    'tipo': row['tipo'],
                    'ativo': int(row['ativo']),
                    'quantidade': float(row['quantidade']),
                    'valor_compra': float(row['valor_compra']),
                    'data': row['data'],
                    'dividendos': float(row.get('dividendos', 0)),
                    'categoria': int(row['categoria']),
                    'corretora': int(row['corretora']),
                }
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                criadas += 1
            except Exception:
                continue

        return Response({'mensagem': f'{criadas} operações importadas com sucesso.'}, status=201)

    @extend_schema(
        summary='Exportar operações do usuário',
        description='Retorna todas as operações do usuário autenticado em formato JSON.',
        responses={200: OpenApiResponse(description='Lista de operações exportadas')}
    )
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        operacoes = self.get_queryset()
        serializer = self.get_serializer(operacoes, many=True)
        return JsonResponse(serializer.data, safe=False)
