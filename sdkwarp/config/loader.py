"""Configuration loader for the SDK."""

import json
import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.config.constants import (
    ENV_PREFIX,
    CONFIG_FILE_PATHS,
    get_default_chain_api,
    get_registry_contract,
    get_chain_id
)

logger = logging.getLogger("sdkwarp.config")


def load_config_from_env() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config_dict = {}
    
    # Chain configuration
    if env := os.environ.get(f"{ENV_PREFIX}ENV"):
        config_dict["env"] = env
    
    if chain_id := os.environ.get(f"{ENV_PREFIX}CHAIN_ID"):
        config_dict["chain_id"] = chain_id
    
    if chain_api_url := os.environ.get(f"{ENV_PREFIX}CHAIN_API_URL"):
        config_dict["chain_api_url"] = chain_api_url
    
    # User configuration
    if user_address := os.environ.get(f"{ENV_PREFIX}USER_ADDRESS"):
        config_dict["user_address"] = user_address
    
    # Wallet configuration
    if wallet_pem_path := os.environ.get(f"{ENV_PREFIX}WALLET_PEM"):
        config_dict["wallet_pem_path"] = wallet_pem_path
    
    if wallet_keystore_path := os.environ.get(f"{ENV_PREFIX}WALLET_KEYSTORE"):
        config_dict["wallet_keystore_path"] = wallet_keystore_path
    
    if wallet_password := os.environ.get(f"{ENV_PREFIX}WALLET_PASSWORD"):
        config_dict["wallet_password"] = wallet_password
    
    if wallet_secret_key := os.environ.get(f"{ENV_PREFIX}WALLET_KEY"):
        config_dict["wallet_secret_key"] = wallet_secret_key
    
    # Registry configuration
    if registry_address := os.environ.get(f"{ENV_PREFIX}REGISTRY_ADDRESS"):
        config_dict["registry_address"] = registry_address
    
    # Cache configuration
    if cache_enabled := os.environ.get(f"{ENV_PREFIX}CACHE_ENABLED"):
        config_dict["cache_enabled"] = cache_enabled.lower() in ("true", "1", "yes")
    
    if cache_ttl := os.environ.get(f"{ENV_PREFIX}CACHE_TTL"):
        try:
            config_dict["cache_ttl"] = int(cache_ttl)
        except ValueError:
            logger.warning(f"Invalid cache TTL value: {cache_ttl}")
    
    return config_dict


def load_config_from_file(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file."""
    if file_path:
        paths = [file_path]
    else:
        paths = CONFIG_FILE_PATHS
    
    for path in paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            try:
                with open(expanded_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Error loading config from {expanded_path}: {e}")
    
    return {}


def get_config(
    env: Optional[Union[str, ChainEnv]] = None,
    user_address: Optional[str] = None,
    chain_api_url: Optional[str] = None,
    config_path: Optional[str] = None,
    **kwargs
) -> Config:
    """Get configuration from multiple sources.
    
    Priority order:
    1. Direct parameters
    2. Environment variables
    3. Configuration file
    4. Default values
    """
    # Load from file
    config_dict = load_config_from_file(config_path)
    
    # Load from environment variables (overrides file)
    env_config = load_config_from_env()
    config_dict.update(env_config)
    
    # Override with direct parameters
    if env is not None:
        config_dict["env"] = env
    
    if user_address is not None:
        config_dict["user_address"] = user_address
    
    if chain_api_url is not None:
        config_dict["chain_api_url"] = chain_api_url
    
    # Add any additional kwargs
    for key, value in kwargs.items():
        if value is not None:
            config_dict[key] = value
    
    # Create config object
    config = Config(**config_dict)
    
    # Set defaults if not provided
    if not config.chain_api_url:
        config.chain_api_url = get_default_chain_api(config.env)
    
    if not config.registry_address:
        config.registry_address = get_registry_contract(config.env)
    
    if not config.chain_id:
        config.chain_id = get_chain_id(config.env)
    
    return config
