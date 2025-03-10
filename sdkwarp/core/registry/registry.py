"""Registry module for interacting with the Warp registry contract."""

import json
import asyncio
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.utils.validation import Validator
from sdkwarp.core.transaction import Transaction
from sdkwarp.utils.encoding import encode_base64, decode_base64


class Registry:
    """Registry for interacting with the Warp registry contract."""

    def __init__(
        self,
        config: Config,
        validator: Optional[Validator] = None
    ):
        """Initialize the registry.

        Args:
            config: SDK configuration
            validator: Validator instance
        """
        self.config = config
        self.validator = validator or Validator()
        self.unit_price = 0
        self._initialized = False

    async def init(self) -> None:
        """Initialize the registry.

        Loads registry configuration from the blockchain.
        """
        await self.load_registry_configs()
        self._initialized = True

    async def load_registry_configs(self) -> None:
        """Load registry configuration from the blockchain."""
        # In a real implementation, this would query the registry contract
        # For now, set a dummy unit price
        self.unit_price = 50000000000000000  # 0.05 EGLD in atomic units

    def create_warp_register_transaction(
        self,
        tx_hash: str,
        alias: Optional[str] = None
    ) -> Transaction:
        """Create a transaction to register a Warp.

        Args:
            tx_hash: Transaction hash of the Warp
            alias: Optional alias for the Warp

        Returns:
            Transaction object

        Raises:
            ValueError: If the registry is not initialized or user address is not set
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Validate transaction hash
        if not self.validator.validate_transaction_hash(tx_hash):
            raise ValueError(f"Invalid transaction hash: {tx_hash}")
        
        # Calculate cost
        cost = self.unit_price * 2 if alias else self.unit_price
        
        # Create function call data
        if alias:
            data = f"registerWarp@{encode_base64(tx_hash)}@{encode_base64(alias)}"
        else:
            data = f"registerWarp@{encode_base64(tx_hash)}"
        
        # Create transaction
        return Transaction(
            sender=self.config.user_address,
            receiver=self.config.registry_address or "",
            value=str(cost),
            data=data,
            gas_limit=10000000,
            chain_id=self.config.chain_id or ""
        )

    def create_warp_unregister_transaction(self, tx_hash: str) -> Transaction:
        """Create a transaction to unregister a Warp.

        Args:
            tx_hash: Transaction hash of the Warp

        Returns:
            Transaction object

        Raises:
            ValueError: If the registry is not initialized or user address is not set
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Validate transaction hash
        if not self.validator.validate_transaction_hash(tx_hash):
            raise ValueError(f"Invalid transaction hash: {tx_hash}")
        
        # Create function call data
        data = f"unregisterWarp@{encode_base64(tx_hash)}"
        
        # Create transaction
        return Transaction(
            sender=self.config.user_address,
            receiver=self.config.registry_address or "",
            value="0",
            data=data,
            gas_limit=10000000,
            chain_id=self.config.chain_id or ""
        )

    async def create_warp_upgrade_transaction(
        self,
        original_tx_hash: str,
        new_tx_hash: str
    ) -> Transaction:
        """Create a transaction to upgrade a Warp.

        Args:
            original_tx_hash: Original transaction hash
            new_tx_hash: New transaction hash

        Returns:
            Transaction object

        Raises:
            ValueError: If the registry is not initialized or user address is not set
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Validate transaction hashes
        if not self.validator.validate_transaction_hash(original_tx_hash):
            raise ValueError(f"Invalid original transaction hash: {original_tx_hash}")
        
        if not self.validator.validate_transaction_hash(new_tx_hash):
            raise ValueError(f"Invalid new transaction hash: {new_tx_hash}")
        
        # Create function call data
        data = f"upgradeWarp@{encode_base64(original_tx_hash)}@{encode_base64(new_tx_hash)}"
        
        # Create transaction
        return Transaction(
            sender=self.config.user_address,
            receiver=self.config.registry_address or "",
            value="0",
            data=data,
            gas_limit=10000000,
            chain_id=self.config.chain_id or ""
        )

    async def get_warp_info(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get information about a Warp.

        Args:
            tx_hash: Transaction hash of the Warp

        Returns:
            Warp information or None if not found
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        # Validate transaction hash
        if not self.validator.validate_transaction_hash(tx_hash):
            raise ValueError(f"Invalid transaction hash: {tx_hash}")
        
        # In a real implementation, this would query the registry contract
        # For now, return a dummy Warp
        return {
            "name": "example-warp",
            "title": "Example Warp",
            "description": "This is an example Warp",
            "action": {
                "type": "transfer",
                "title": "Transfer EGLD",
                "description": "Transfer EGLD to an address",
                "data": {
                    "token": "EGLD",
                    "amount": "0.1",
                    "recipient": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
                }
            },
            "metadata": {
                "hash": tx_hash,
                "creator": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                "createdAt": "2023-01-01T00:00:00Z"
            }
        }

    async def get_warp_by_alias(self, alias: str) -> Optional[Dict[str, Any]]:
        """Get a Warp by its alias.

        Args:
            alias: Warp alias

        Returns:
            Warp information or None if not found
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        # In a real implementation, this would query the registry contract
        # For now, return a dummy Warp
        return {
            "name": alias,
            "title": f"Warp {alias}",
            "description": f"This is the Warp with alias {alias}",
            "action": {
                "type": "transfer",
                "title": "Transfer EGLD",
                "description": "Transfer EGLD to an address",
                "data": {
                    "token": "EGLD",
                    "amount": "0.1",
                    "recipient": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
                }
            },
            "metadata": {
                "hash": "dummy_hash_for_" + alias,
                "creator": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                "createdAt": "2023-01-01T00:00:00Z"
            }
        }

    async def get_registry_info(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get registry information for a Warp.

        Args:
            tx_hash: Transaction hash of the Warp

        Returns:
            Registry information or None if not found
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        # Validate transaction hash
        if not self.validator.validate_transaction_hash(tx_hash):
            raise ValueError(f"Invalid transaction hash: {tx_hash}")
        
        # In a real implementation, this would query the registry contract
        # For now, return dummy registry info
        return {
            "hash": tx_hash,
            "alias": "example-warp",
            "trust": "verified",
            "creator": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
            "createdAt": 1672531200,  # 2023-01-01T00:00:00Z
            "brand": None,
            "upgrade": None
        }

    async def get_brand_info(self, brand_hash: str) -> Optional[Dict[str, Any]]:
        """Get information about a brand.

        Args:
            brand_hash: Brand hash

        Returns:
            Brand information or None if not found
        """
        if not self._initialized:
            raise ValueError("Registry not initialized. Call init() first.")
        
        # Validate transaction hash (brand hash is also a transaction hash)
        if not self.validator.validate_transaction_hash(brand_hash):
            raise ValueError(f"Invalid brand hash: {brand_hash}")
        
        # In a real implementation, this would query the registry contract
        # For now, return a dummy brand
        return {
            "name": "example-brand",
            "description": "This is an example brand",
            "logo": "https://example.com/logo.png",
            "urls": {
                "web": "https://example.com"
            },
            "colors": {
                "primary": "#FF0000",
                "secondary": "#00FF00"
            },
            "cta": {
                "title": "Visit Website",
                "description": "Visit our website to learn more",
                "label": "Visit",
                "url": "https://example.com"
            },
            "metadata": {
                "hash": brand_hash,
                "creator": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                "createdAt": "2023-01-01T00:00:00Z"
            }
        }
