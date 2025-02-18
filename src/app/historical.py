import os
import glob
import pandas as pd
from web3 import Web3
from app.sqlite import check_if_account_balances_exist, get_account_balance_history
from app.token import update_account_balances


def update_historical_prices_and_balances(w3: Web3, network: str):
    df_historical = _import_historical_data()

    for index, row in df_historical.iterrows():
        if not check_if_account_balances_exist(row["owner"], row["block_number"], network):
            update_account_balances(w3, row["owner"], network, row["block_number"])

    df = get_account_balance_history(row["owner"], network)
    print(df)



    # print(df_historical)


def _import_historical_data() -> pd.DataFrame:
    ''' Make sure that the file has this filename format:
        "export-0x1D1479C185d32EB90533a08b36B3CFa5F84A0E6B.csv"
    '''
    # Define directory containing CSV files
    csv_directory = "historical/"

    # List all CSV files in the directory
    csv_files = glob.glob(os.path.join(csv_directory, "*.csv"))

    historical_data = []

    for file in csv_files:
        print(f"Processing: {file}")

        # Extract Ethereum address from filename
        filename = os.path.basename(file)
        address = filename.split("-")[1].split(".csv")[0]

        # Read CSV
        df = pd.read_csv(file)

        assert Web3.is_address(address), f"Invalid Ethereum address: {address}"
        assert "UnixTimestamp" in df.columns, f"Missing UnixTimestamp column in {file}"
        assert "Blockno" in df.columns, f"Missing Blockno column in {file}"

        # Convert timestamps & block numbers to integers
        df["timestamp"] = df["UnixTimestamp"].astype(int)
        df["block_number"] = df["Blockno"].astype(int)

        # Add wallet address column
        df["owner"] = address

        # Append to historical data
        historical_data.append(df[["timestamp", "block_number", "owner"]])

    # Combine all data into a single DataFrame
    df_historical = pd.concat(historical_data, ignore_index=True)

    df_historical = df_historical.drop_duplicates().reset_index(drop=True)

    return df_historical
