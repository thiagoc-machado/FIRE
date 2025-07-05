from celery import shared_task
from core.models import Asset
from core.services.yahoo_service import buscar_dados_ativo

@shared_task
def atualizar_cotacoes_ativos():
    for asset in Asset.objects.all():
        dados = buscar_dados_ativo(asset.codigo)
        if dados['cotacao']:
            asset.nome = dados['nome']
            asset.moeda = dados['moeda']
            asset.dividend_yield = dados['dividend_yield']
            asset.frequencia_dividendos = dados['frequencia']
            asset.save()
            