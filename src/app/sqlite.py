import os
import sqlite3
import pandas as pd
import rubik as rk


# Ensure the db folder exists
DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "portfolio_tracker.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)  # Create the directory if it doesn't exist

def setup_sqlite():
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS aave_trades (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         timestamp INTEGER,
    #         block_number INTEGER,
    #         network TEXT,
    #         owner TEXT,
    #         token_symbol TEXT,
    #         token_desc TEXT,
    #         token_address TEXT,
    #         decimals INTEGER,
    #         balance TEXT
    #     )
    # """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            block_number INTEGER,
            network TEXT,
            owner TEXT,
            token_symbol TEXT,
            token_desc TEXT,
            token_address TEXT,
            balance TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS valkyrie_one_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            block_number INTEGER,
            credit_balance TEXT,
            debit_balance TEXT,
            total_balance TEXT
        )
    """)

    # Create token_prices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            token_symbol TEXT,
            price_usd_8_decimals TEXT
        )
    """)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("✅ SQLite setup completed!")


def check_if_account_balances_exist(wallet_address: str, block_number: int, network: str = "arbitrum") -> bool:
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    query = f"""
        SELECT COUNT(*)
        FROM account_balances
        WHERE owner = '{wallet_address}' AND block_number = {block_number} AND network = '{network}';
    """

    # Query latest token prices
    cursor = conn.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]

    # Close connection
    conn.close()

    return count > 0


def store_token_prices(df: pd.DataFrame):
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert new row
    df.to_sql("token_prices", conn, if_exists="append", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("✅ Token Prices updated in SQLite!")


def get_latest_token_prices() -> pd.DataFrame:
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT token_symbol, price_usd_8_decimals, timestamp
        FROM token_prices
        WHERE timestamp = (
            SELECT MAX(timestamp)
            FROM token_prices AS t
            WHERE t.token_symbol = token_prices.token_symbol
        )
        ORDER BY token_symbol;
    """

    # Query latest token prices
    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    # Notice, keep the balances as strings when using pandas 🐼.
    # df["price_usd_8_decimals"] = df["price_usd_8_decimals"].astype(int)

    return df


def store_account_balances(df: pd.DataFrame):
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert new row
    df.to_sql("account_balances", conn, if_exists="append", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("✅ Account Balances updated in SQLite!")


def get_latest_account_balances(wallet_address: str, network: str = "arbitrum") -> pd.DataFrame:
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    query = f"""
        SELECT *
        FROM account_balances
        WHERE timestamp = (
            SELECT MAX(timestamp)
            FROM account_balances AS t
            WHERE t.token_symbol = account_balances.token_symbol AND owner = '{wallet_address}' AND network = '{network}'
        )
        ORDER BY token_symbol;
    """

    # Query latest token prices
    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    return df


def get_account_balance_history(wallet_address: str, network: str = "arbitrum") -> pd.DataFrame:
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    query = f"""
        SELECT *
        FROM account_balances
        WHERE owner = '{wallet_address}' AND network = '{network}'
        ORDER BY timestamp;
    """

    # Query latest token prices
    df = pd.read_sql(query, conn).drop(columns=["id"])

    # Close connection
    conn.close()

    df = rk.groupto_dict(df, ["token_symbol", "token_desc", "token_address", "balance"], "tokens")
    df = rk.groupto_list(df, ["timestamp", "block_number", "network", "owner"], "tokens")

    return df
