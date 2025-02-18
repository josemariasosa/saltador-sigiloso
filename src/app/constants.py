import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read secrets
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
ALPHA_CENTAURI_ADDRESS = os.getenv("ALPHA_CENTAURI_ADDRESS")
VALKYRIE_ONE_ADDRESS = os.getenv("VALKYRIE_ONE_ADDRESS")

NETWORKS = {
    "arbitrum": "https://arbitrum-mainnet.infura.io/v3/",
    "mainnet": "https://mainnet.infura.io/v3/",
}

TOKENS = {
    "arbitrum": {
        "wbtc": {
            "addresses" : {
                "native": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
                "aave": "0x078f358208685046a11C85e8ad32895DED33A249",
            },
            "coingecko": "wrapped-bitcoin",
            "decimals": 8,
            "category": "bitcoin",
        },
        "eth": {
            "coingecko": "ethereum",
            "decimals": 18,
            "category": "ethereum",
        },
        "weth": {
            "addresses" : {
                "native": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                "aave": "0xe50fA9b3c56FfB159cB0FCA61F5c9D750e8128c8",
            },
            "coingecko": "weth",
            "decimals": 18,
            "category": "ethereum",
        },
        "usdt": {
            "addresses" : {
                "native": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
                "aave": "0x6ab707Aca953eDAeFBc4fD23bA73294241490620",
                "aaveDebt": "0xfb00AC187a8Eb5AFAE4eACE434F493Eb62672df7",
            },
            "coingecko": "tether",
            "decimals": 6,
            "category": "stablecoin",
        },
        "usdc": {
            "addresses" : {
                "native": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                "aave": "0x724dc807b04555b71ed48a6896b6F41593b8C637",
                "aaveDebt": "0xf611aEb5013fD2c0511c9CD55c7dc5C1140741A6",
            },
            "coingecko": "usd-coin",
            "decimals": 6,
            "category": "stablecoin",
        },
        "dai": {
            "addresses" : {
                "native": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
                "aave": "0x82E64f49Ed5EC1bC6e43DAD4FC8Af9bb3A2312EE",
            },
            "coingecko": "dai",
            "decimals": 18,
            "category": "stablecoin",
        },
        "arb": {
            "addresses" : {
                "native": "0x912ce59144191c1204e64559fe8253a0e49e6548",
                "aave": "0x6533afac2E7BCCB20dca161449A13A32D391fb00",
            },
            "coingecko": "arbitrum",
            "decimals": 18,
            "category": "altcoin",
        },
        "link": {
            "addresses" : {
                "native": "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4",
                "aave": "0x191c10Aa4AF7C30e871E70C95dB0E4eb77237530",
            },
            "coingecko": "chainlink",
            "decimals": 18,
            "category": "altcoin",
        },
        "gho": {
            "addresses" : {
                "native": "0x7dfF72693f6A4149b17e7C6314655f6A9F7c8B33",
                "aave": "0xeBe517846d0F36eCEd99C735cbF6131e1fEB775D",
                "aaveDebt": "0x18248226C16BF76c032817854E7C83a2113B4f06",
            },
            "coingecko": "gho",
            "decimals": 18,
            "category": "stablecoin",
        },
    },
}