from app.constants import TOKENS
from app.utils import get_abi
from app.sqlite import store_account_balances
from web3 import Web3
from datetime import datetime

import pandas as pd


def update_account_balances(w3: Web3, wallet_address: str, network: str, block_number = 'latest'):
    if block_number == 'latest':
        block_number = w3.eth.block_number

    # Fetch block details
    block = w3.eth.get_block(block_number)

    data = pd.DataFrame(
        get_token_balances(w3, wallet_address, network, block)
        + [get_native_token_balance(w3, wallet_address, network, block)]
    )

    store_account_balances(data)


def get_token_balances(w3: Web3, wallet_address: str, network: str, block) -> list:
    if network not in TOKENS.keys():
        raise ValueError(f"Network {network} not found in TOKENS")

    tokens = TOKENS[network]
    erc20_abi = get_abi("Token")

    data = []
    for ticker, token in tokens.items():
        token_addresses: dict = token.get("addresses", {})
        for desc, address in token_addresses.items():
            token_contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=erc20_abi)

            try:
                balance = token_contract.functions.balanceOf(
                    Web3.to_checksum_address(wallet_address)
                ).call(block_identifier=block.number)
            except:
                balance = 0

            data.append({
                "timestamp": block.timestamp,
                "block_number": block.number,
                "network": network,
                "owner": wallet_address,
                "token_symbol": ticker,
                "token_desc": desc,
                "token_address": address,
                "balance": str(balance),
            })

    return data


def get_native_token_balance(w3: Web3, wallet_address: str, network: str, block) -> dict:
    return {
        "timestamp": block.timestamp,
        "block_number": block.number,
        "network": network,
        "owner": wallet_address,
        "token_symbol": "eth",
        "token_desc": "native",
        "token_address": None,
        "balance": str(w3.eth.get_balance(
            Web3.to_checksum_address(wallet_address),
            block_identifier=block.number)
        ),
    }


def update_credit_debit(wallet_address: str, balances: pd.DataFrame):
    mask = balances["token_desc"].str.endswith("Debt")
    credit_balance = balances[mask]["total_usd"].astype(float).sum()
    debit_balance = balances[~mask]["total_usd"].astype(float).sum()
    total_balance = debit_balance - credit_balance

    print(f"Credit: {credit_balance}")
    print(f"Debit: {debit_balance}")
    print(f"Total: {total_balance}")

    # conn = sqlite3.connect(DB_PATH)
    # cursor = conn.cursor()

    # cursor.execute("""
    #     INSERT INTO valkyrie_one_balances (timestamp, credit_balance, debit_balance, total_balance)
    #     VALUES (?, ?, ?, ?)
    # """, (datetime.now(), str(credit_balance), str(debit_balance), str(total_balance)))

    # conn.commit()
    # conn.close()