import os
import sqlite3
import pandas as pd

# Ensure the db folder exists
DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "portfolio_tracker.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)  # Create the directory if it doesn't exist

def setup_sqlite():
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eth_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            eth_address TEXT,
            eth_balance TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS valkyrie_one_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            eth_balance TEXT,
            wbtc_balance TEXT,
            weth_balance TEXT,
            usdt_balance TEXT,
            usdc_balance TEXT,
            dai_balance TEXT,
            arb_balance TEXT,
            link_balance TEXT,
            gho_balance TEXT,
            total_usd_value TEXT
        )
    """)

    # Create token_prices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            token_symbol TEXT,
            price_usd_8_decimals TEXT
        )
    """)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("✅ SQLite setup completed!")


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

    df["price_usd_8_decimals"] = df["price_usd_8_decimals"].astype(int)

    # Close connection
    conn.close()

    return df
