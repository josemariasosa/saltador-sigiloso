from app.eth_provider import get_provider
from app.sqlite import get_latest_account_balances, get_latest_token_prices, setup_sqlite, DB_PATH
from app.price_feed import update_token_prices
from app.constants import ALPHA_CENTAURI_ADDRESS, VALKYRIE_ONE_ADDRESS
from app.token import update_account_balances, update_credit_debit
from app.utils import calculate_total_usd

from datetime import datetime
from web3 import Web3

import os
import pandas as pd
import sqlite3


def main(update_prices: bool = False, update_balances: bool = False):
# def main(update_prices: bool = True, update_balances: bool = True):

    setup_sqlite()

    if update_prices:
        update_token_prices()

    if update_balances:
        w3 = get_provider("arbitrum")
        update_account_balances(w3, VALKYRIE_ONE_ADDRESS)

    prices = get_latest_token_prices()
    balances = get_latest_account_balances(VALKYRIE_ONE_ADDRESS)

    balances = balances.merge(prices.drop(columns=["timestamp"]), on="token_symbol", how="left")
    balances["total_usd"] = balances.apply(lambda row: calculate_total_usd(row), axis=1)


    print(prices)
    print("---------------------")
    print(balances.drop(columns=["owner", "timestamp", "token_address"]))

    update_credit_debit(VALKYRIE_ONE_ADDRESS, balances)



    # data = get_data(w3)

    # store_data(data)

    # print("🚀 Done!")

    # query_data()





def store_data(df: pd.DataFrame):
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert new row
    df.to_sql("eth_balances", conn, if_exists="append", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("✅ Data stored successfully in SQLite!")


def query_data():
    # Reconnect to database
    conn = sqlite3.connect(DB_PATH)

    # Read table
    df_check = pd.read_sql("SELECT * FROM eth_balances", conn)

    # Display
    print(df_check)

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()