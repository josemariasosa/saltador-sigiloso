from app.constants import TOKENS
from app.sqlite import store_token_prices, DB_PATH
from datetime import datetime

import requests
import pandas as pd


def get_defillama_price_8_decimals(symbol):
    url = f"https://coins.llama.fi/prices/current/coingecko:{symbol.lower()}"
    response = requests.get(url)
    data = response.json()
    if "coins" in data and f"coingecko:{symbol.lower()}" in data["coins"]:
        price = data["coins"][f"coingecko:{symbol.lower()}"]["price"]
        price_chainlink_format = int(price * 10**8)  # Convert to 8 decimals
        price_as_string = str(price_chainlink_format)  # Convert to string
        return price_as_string
    return None


def update_token_prices(network: str = "arbitrum"):
    ''' token_prices table:
        timestamp TEXT,
        token_symbol TEXT,
        price_usd_8_decimals TEXT
    '''
    now = datetime.now()
    prices = []
    for ticker, value in TOKENS[network].items():
        prices.append({
            "timestamp": now,
            "token_symbol": ticker.lower(),
            "price_usd_8_decimals": get_defillama_price_8_decimals(value['coingecko'])
        })

    df = pd.DataFrame(prices)
    store_token_prices(df)
    