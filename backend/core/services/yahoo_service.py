import yfinance as yf

def buscar_dados_ativo(codigo):
    ativo = yf.Ticker(codigo)
    try:
        cotacao = ativo.history(period='1d')['Close'].iloc[-1]
    except Exception:
        cotacao = None

    info = ativo.info

    return {
        'cotacao': cotacao,
        'moeda': info.get('currency'),
        'dividend_yield': info.get('dividendYield'),
        'frequencia': info.get('dividendRate'),
        'nome': info.get('shortName'),
    }