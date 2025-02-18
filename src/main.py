from app.eth_provider import get_provider
from app.sqlite import get_latest_account_balances, get_latest_token_prices, setup_sqlite, DB_PATH
from app.price_feed import update_token_prices
from app.constants import ALPHA_CENTAURI_ADDRESS, VALKYRIE_ONE_ADDRESS
from app.token import update_account_balances, update_credit_debit
from app.utils import calculate_total_usd
from app.historical import update_historical_prices_and_balances

from datetime import datetime
from web3 import Web3

import os
import pandas as pd
import sqlite3


CONFIG = {
    "update_historical": True,
    "update_prices": False,
    "update_balances": False,
    "network": "arbitrum"
}

def main(config: dict = CONFIG):

    setup_sqlite()
    w3 = get_provider(config["network"])

    if config["update_historical"]:
        update_historical_prices_and_balances(w3, config["network"])



    # if update_prices:
    #     update_token_prices()

    # if update_balances:
    #     w3 = get_provider("arbitrum")
    #     update_account_balances(w3, VALKYRIE_ONE_ADDRESS)

    # prices = get_latest_token_prices()
    # balances = get_latest_account_balances(VALKYRIE_ONE_ADDRESS)

    # balances = balances.merge(prices.drop(columns=["timestamp"]), on="token_symbol", how="left")
    # balances["total_usd"] = balances.apply(lambda row: calculate_total_usd(row), axis=1)


    # print(prices)
    # print("---------------------")
    # print(balances.drop(columns=["owner", "timestamp", "token_address"]))

    # update_credit_debit(VALKYRIE_ONE_ADDRESS, balances)









if __name__ == "__main__":
    main()