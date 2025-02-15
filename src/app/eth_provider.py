from app.constants import INFURA_PROJECT_ID, NETWORKS
from web3 import Web3


def get_provider(network: str, api_key: str = None) -> Web3:
    if network not in NETWORKS.keys():
        raise ValueError(f"Invalid network: {network}")
    
    if api_key is None:
        api_key = INFURA_PROJECT_ID

    infura_url = f"{NETWORKS[network]}{api_key}"
    w3 = Web3(Web3.HTTPProvider(infura_url))

    # Check if connected
    if w3.is_connected():
        print("✅ Successfully connected to Ethereum Mainnet!")
    else:
        print("❌ Connection failed!")
    
    return w3