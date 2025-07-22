import yfinance as yf
import requests
import json
from time import sleep

OUTPUT_FILE = 'symbols_database.json'

# === Buscar criptos (CoinGecko) ===
def fetch_cryptos(limit=500):
    print('🔄 Buscando criptomoedas do CoinGecko...')
    cryptos = []
    per_page = 250
    pages = (limit + per_page - 1) // per_page

    for page in range(1, pages + 1):
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': page
        }
        try:
            response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=params)
            response.raise_for_status()
            for coin in response.json():
                cryptos.append({
                    'codigo': f"{coin['symbol'].upper()}-USD",
                    'nome': coin['name'],
                    'tipo': 'Cryptocurrency',
                    'categoria': 'Digital Assets'
                })
            sleep(1)
        except Exception as e:
            print(f'⚠️ Erro CoinGecko página {page}: {e}')
    return cryptos

# === Buscar ativos via Yahoo Finance ===
def fetch_yf_assets(tickers, tipo_padrao='Stock'):
    print(f'🔄 Buscando {len(tickers)} ativos do Yahoo Finance...')
    assets = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            nome = info.get('shortName') or info.get('longName') or ticker
            categoria = info.get('sector', 'Outro') or 'Outro'
            tipo = 'ETF' if 'ETF' in info.get('longBusinessSummary', '') else tipo_padrao

            assets.append({
                'codigo': ticker,
                'nome': nome,
                'tipo': tipo,
                'categoria': categoria
            })
        except Exception as e:
            print(f'⚠️ Erro ao buscar {ticker}: {e}')
        sleep(0.3)  # evitar bloqueio do Yahoo
    return assets

# === Função genérica para carregar CSVs de tickers ===
def load_tickers_from_csv(url, coluna='Symbol', sufixo=''):
    print(f'🌐 Carregando tickers de: {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        header = lines[0].split(',')
        idx = header.index(coluna)
        tickers = [line.split(',')[idx] + sufixo for line in lines[1:] if line]
        return tickers
    except Exception as e:
        print(f'⚠️ Erro ao carregar CSV: {e}')
        return []

def load_global_tickers():
    tickers = []

    # ✅ S&P500
    tickers += load_tickers_from_csv(
        'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    )

    # ✅ Nasdaq 100 (fonte alternativa)
    tickers += load_tickers_from_csv(
        'https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/NASDAQ%20100%20Constituents%20(Nasdaq)/NASDAQ%20100%20Constituents%20(Nasdaq).csv',
        coluna='ticker'
    )

    # ✅ Dow Jones (manual)
    tickers += [
        'AAPL', 'MSFT', 'JNJ', 'V', 'WMT', 'UNH', 'PG', 'JPM', 'HD', 'INTC',
        'KO', 'MRK', 'DIS', 'MCD', 'IBM', 'CAT', 'NKE', 'AXP', 'CVX', 'GS',
        'TRV', 'VZ', 'BA', 'AMGN', 'DOW', 'MMM', 'CSCO', 'CRM', 'HON', 'WBA'
    ]

    # ✅ FTSE 100 (fonte alternativa)
    tickers += load_tickers_from_csv(
        'https://raw.githubusercontent.com/n0shake/public-assets/master/ftse100/constituents.csv',
        coluna='Ticker',
        sufixo='.L'
    )

    return list(set(tickers))


# === Construir e salvar o JSON final ===
def build_symbols_json():
    symbols = []

    # Criptos
    symbols += fetch_cryptos(limit=500)

    # Ações globais
    global_tickers = load_global_tickers()
    symbols += fetch_yf_assets(global_tickers)

    # Ações brasileiras opcionais
    br_tickers = ['VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'WEGE3.SA']
    symbols += fetch_yf_assets(br_tickers)

    # Salvar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(symbols, f, indent=4, ensure_ascii=False)

    print(f'\n✅ Arquivo "{OUTPUT_FILE}" gerado com {len(symbols)} ativos.')

# === Início ===
if __name__ == '__main__':
    build_symbols_json()
