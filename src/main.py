from app.eth_provider import get_provider
from app.sqlite import get_latest_token_prices, setup_sqlite, DB_PATH
from app.price_feed import update_token_prices
from app.constants import ALPHA_CENTAURI_ADDRESS

from datetime import datetime
from dotenv import load_dotenv
from web3 import Web3

import os
import pandas as pd
import sqlite3

# Load .env file
load_dotenv()


def main(update_prices: bool = False):

    setup_sqlite()

    if update_prices:
        update_token_prices()

    prices = get_latest_token_prices()

    print(prices)
    # w3 = get_provider("arbitrum")
    # data = get_data(w3)

    # store_data(data)

    # print("🚀 Done!")

    # query_data()


def get_data(w3: Web3):
    eth_address = ALPHA_CENTAURI_ADDRESS

    # Get ETH balance (returns balance in Wei)
    balance_wei = w3.eth.get_balance(eth_address)

    # Convert to ETH
    balance_eth = w3.from_wei(balance_wei, 'ether')

    print(f"ETH Balance for {eth_address}: {balance_eth} ETH")


    # Create a DataFrame with timestamp and balance
    data = {
        "timestamp": [datetime.now()],
        "eth_address": [eth_address],
        "eth_balance": [balance_wei]
    }

    df = pd.DataFrame(data)

    # Show table
    print(df)

    return df


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