"""Validation utilities for the SDK."""

import re
import json
from typing import Any, Dict, List, Optional, Union

from sdkwarp.config.models import Config


class Validator:
    """Validation utilities."""
    
    def __init__(self, config: Config):
        """Initialize validator.
        
        Args:
            config: SDK configuration
        """
        self.config = config
    
    def validate_address(self, address: str) -> bool:
        """Validate MultiversX address.
        
        Args:
            address: Address to validate
        
        Returns:
            True if address is valid, False otherwise
        """
        # MultiversX addresses start with "erd1" and are 62 characters long
        return bool(re.match(r"^erd1[a-zA-Z0-9]{58}$", address))
    
    def validate_transaction_hash(self, tx_hash: str) -> bool:
        """Validate transaction hash.
        
        Args:
            tx_hash: Transaction hash to validate
        
        Returns:
            True if transaction hash is valid, False otherwise
        """
        # Transaction hashes are 64 hex characters
        return bool(re.match(r"^[a-fA-F0-9]{64}$", tx_hash))
    
    def validate_warp_schema(self, warp: Dict[str, Any]) -> bool:
        """Validate Warp schema.
        
        Args:
            warp: Warp object to validate
        
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
    
    def validate_brand(self, brand: Dict[str, Any]) -> bool:
        """Validate brand schema.
        
        Args:
            brand: Brand object to validate
        
        Returns:
            True if brand schema is valid, False otherwise
        """
        # Basic validation
        if not isinstance(brand, dict):
            return False
        
        # Required fields
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in brand:
                return False
        
        # Optional fields validation
        if "urls" in brand and not isinstance(brand["urls"], dict):
            return False
        
        if "colors" in brand and not isinstance(brand["colors"], dict):
            return False
        
        if "cta" in brand and not isinstance(brand["cta"], dict):
            return False
        
        return True
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration.
        
        Args:
            config: Configuration to validate
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Basic validation
        if not isinstance(config, dict):
            return False
        
        # Environment validation
        if "env" in config and config["env"] not in ["devnet", "testnet", "mainnet"]:
            return False
        
        # User address validation
        if "user_address" in config and not self.validate_address(config["user_address"]):
            return False
        
        # Registry address validation
        if "registry_address" in config and not self.validate_address(config["registry_address"]):
            return False
        
        return True
