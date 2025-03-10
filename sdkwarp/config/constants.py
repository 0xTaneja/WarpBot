"""Configuration constants for the SDK."""

from typing import Dict, Optional

from sdkwarp.config.models import ChainEnv

# Chain IDs
DEVNET_CHAIN_ID = "D"
TESTNET_CHAIN_ID = "T"
MAINNET_CHAIN_ID = "1"
METACHAIN_ID = "4294967295"

# Network provider URLs
NETWORK_PROVIDER_URLS: Dict[ChainEnv, str] = {
    ChainEnv.DEVNET: "https://devnet-api.multiversx.com",
    ChainEnv.TESTNET: "https://testnet-api.multiversx.com",
    ChainEnv.MAINNET: "https://api.multiversx.com"
}

# Registry contract addresses
REGISTRY_CONTRACT_ADDRESSES: Dict[ChainEnv, str] = {
    ChainEnv.DEVNET: "erd1qqqqqqqqqqqqqpgqd9rvv2n378e27jcts8vfwynpx0gfl5ufz6hqhfy0u0",
    ChainEnv.TESTNET: "erd1qqqqqqqqqqqqqpgq705fxpfrjne0tl3ece0rrspykq88mynn4kxs2cg43s",
    ChainEnv.MAINNET: "erd1qqqqqqqqqqqqqpgq6wegs2xkypfpync8mn2sa5cmpqjlvl2yj7kqtpylm3"
}

# Environment variable prefixes
ENV_PREFIX = "WARP_"

# Config file paths
CONFIG_FILE_PATHS = [
    "./warp.config.json",
    "~/.warp/config.json"
]


def get_default_chain_api(env: ChainEnv) -> str:
    """Get default chain API URL for environment."""
    return NETWORK_PROVIDER_URLS.get(env, NETWORK_PROVIDER_URLS[ChainEnv.DEVNET])


def get_registry_contract(env: ChainEnv) -> Optional[str]:
    """Get registry contract address for environment."""
    return REGISTRY_CONTRACT_ADDRESSES.get(env)


def get_chain_id(env: ChainEnv) -> str:
    """Get chain ID for environment."""
    if env == ChainEnv.DEVNET:
        return DEVNET_CHAIN_ID
    elif env == ChainEnv.TESTNET:
        return TESTNET_CHAIN_ID
    elif env == ChainEnv.MAINNET:
        return MAINNET_CHAIN_ID
    else:
        return DEVNET_CHAIN_ID
