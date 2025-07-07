import yfinance as yf
from datetime import datetime, timedelta

def buscar_dados_ativo(codigo):
    ativo = yf.Ticker(codigo)

    # Tentativa de cotação atual
    try:
        cotacao = ativo.history(period='1d')['Close'].iloc[-1]
    except Exception:
        cotacao = None

    # Informações básicas
    info = ativo.info

    # Histórico de dividendos
    dividendos = ativo.dividends

    # Remove o timezone do índice
    dividendos.index = dividendos.index.tz_localize(None)

    hoje = datetime.today()
    um_ano_atras = hoje - timedelta(days=365)

    # Filtra dividendos nos últimos 12 meses
    dividendos_ultimo_ano = dividendos[dividendos.index > um_ano_atras]

    frequencia_estimativa = len(dividendos_ultimo_ano)

    return {
        'codigo': codigo.upper(),
        'nome': info.get('shortName'),
        'cotacao': cotacao,
        'moeda': info.get('currency'),
        'dividend_yield': info.get('dividendYield'),
        'frequencia': frequencia_estimativa,
        'tipo': info.get('quoteType') or info.get('typeDisp'),
        'categoria': info.get('category'),
    }
