import json
from app.constants import TOKENS

import pandas as pd


def get_abi(contract_name):
    with open(f"out/{contract_name}.sol/{contract_name}.json") as f:
        abi = json.load(f)["abi"]
        print(f"✅ {contract_name} ABI Loaded Successfully!")
        return abi


def calculate_total_usd(row):
    balance = int(row["balance"])
    price = int(row["price_usd_8_decimals"])
    decimals = row["decimals"]

    total_usd = (balance * price) / 10 ** (decimals + 8)
    return "{:.2f}".format(total_usd)


def get_token_details(network: str = "arbitrum") -> pd.DataFrame:
    tokens = TOKENS[network]
    data = []
    for ticker, token in tokens.items():
        data.append({
            "token_symbol": ticker,
            "decimals": token.get("decimals"),
            "category": token.get("category"),
        })
    return pd.DataFrame(data)
