"""General purpose helper functions for the SDK."""

import re
import os
import json
from typing import Any, Dict, List, Optional, Union

from sdkwarp.config.models import ChainEnv


def build_client_url(base_url: str, path: str) -> str:
    """Build client URL.
    
    Args:
        base_url: Base URL
        path: Path to append
    
    Returns:
        Complete URL
    """
    # Ensure base_url doesn't end with slash and path starts with slash
    base_url = base_url.rstrip("/")
    path = f"/{path.lstrip('/')}"
    
    return f"{base_url}{path}"


def build_validator_url(base_url: str) -> str:
    """Build validator URL.
    
    Args:
        base_url: Base URL
    
    Returns:
        Validator URL
    """
    return build_client_url(base_url, "validator")


def verify_warp_schema(warp: Dict[str, Any]) -> bool:
    """Verify Warp schema.
    
    Args:
        warp: Warp object to verify
    
    Returns:
        True if Warp schema is valid, False otherwise
    """
    # Basic validation
    if not isinstance(warp, dict):
        return False
    
    # Required fields
    required_fields = ["name", "title", "description", "action"]
    for field in required_fields:
        if field not in warp:
            return False
    
    # Action validation
    action = warp.get("action", {})
    if not isinstance(action, dict):
        return False
    
    # Action required fields
    action_required_fields = ["type", "title", "description"]
    for field in action_required_fields:
        if field not in action:
            return False
    
    # Action type validation
    action_type = action.get("type")
    if action_type not in ["transfer", "contract", "query", "collect"]:
        return False
    
    return True


def is_valid_address(address: str) -> bool:
    """Check if address is valid.
    
    Args:
        address: Address to check
    
    Returns:
        True if address is valid, False otherwise
    """
    # MultiversX addresses start with "erd1" and are 62 characters long
    return bool(re.match(r"^erd1[a-zA-Z0-9]{58}$", address))


def is_valid_transaction_hash(tx_hash: str) -> bool:
    """Check if transaction hash is valid.
    
    Args:
        tx_hash: Transaction hash to check
    
    Returns:
        True if transaction hash is valid, False otherwise
    """
    # Transaction hashes are 64 hex characters
    return bool(re.match(r"^[a-fA-F0-9]{64}$", tx_hash))


def get_env_from_string(env_str: str) -> ChainEnv:
    """Get ChainEnv from string.
    
    Args:
        env_str: Environment string
    
    Returns:
        ChainEnv value
    """
    env_str = env_str.lower()
    
    if env_str in ["devnet", "dev"]:
        return ChainEnv.DEVNET
    elif env_str in ["testnet", "test"]:
        return ChainEnv.TESTNET
    elif env_str in ["mainnet", "main"]:
        return ChainEnv.MAINNET
    else:
        return ChainEnv.DEVNET


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        JSON data
    """
    try:
        with open(os.path.expanduser(file_path), "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise ValueError(f"Error loading JSON file {file_path}: {e}")


def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """Save JSON file.
    
    Args:
        file_path: Path to JSON file
        data: Data to save
    """
    try:
        with open(os.path.expanduser(file_path), "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        raise ValueError(f"Error saving JSON file {file_path}: {e}")
