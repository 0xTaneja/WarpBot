"""Index module for querying the Warp registry index."""

import json
import asyncio
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.utils.validation import Validator


class Index:
    """Index for querying the Warp registry index."""

    def __init__(
        self,
        config: Config,
        validator: Optional[Validator] = None
    ):
        """Initialize the index.

        Args:
            config: SDK configuration
            validator: Validator instance
        """
        self.config = config
        self.validator = validator or Validator()
        self._initialized = False
        self._index_url = None

    async def init(self) -> None:
        """Initialize the index.

        Sets up the index URL based on the configuration.
        """
        env = self.config.env or ChainEnv.DEVNET
        
        # Set index URL based on environment
        if env == ChainEnv.MAINNET:
            self._index_url = "https://index.warp.multiversx.com"
        elif env == ChainEnv.TESTNET:
            self._index_url = "https://testnet-index.warp.multiversx.com"
        else:  # DEVNET
            self._index_url = "https://devnet-index.warp.multiversx.com"
        
        self._initialized = True

    async def get_warps(
        self,
        limit: int = 10,
        offset: int = 0,
        creator: Optional[str] = None,
        sort: str = "createdAt",
        order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get a list of Warps from the index.

        Args:
            limit: Maximum number of Warps to return
            offset: Offset for pagination
            creator: Filter by creator address
            sort: Sort field
            order: Sort order (asc or desc)

        Returns:
            List of Warps

        Raises:
            ValueError: If the index is not initialized
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # Validate parameters
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValueError("Offset must be non-negative")
        
        if creator and not self.validator.validate_address(creator):
            raise ValueError(f"Invalid creator address: {creator}")
        
        if sort not in ["createdAt", "name", "title"]:
            raise ValueError(f"Invalid sort field: {sort}")
        
        if order not in ["asc", "desc"]:
            raise ValueError(f"Invalid order: {order}")
        
        # In a real implementation, this would query the index API
        # For now, return dummy Warps
        return [
            {
                "name": f"example-warp-{i}",
                "title": f"Example Warp {i}",
                "description": f"This is example Warp {i}",
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
                    "hash": f"dummy_hash_{i}",
                    "creator": creator or "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                    "createdAt": f"2023-01-0{i+1}T00:00:00Z"
                }
            }
            for i in range(offset, offset + limit)
        ]

    async def get_warp(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get a Warp by its transaction hash.

        Args:
            tx_hash: Transaction hash of the Warp

        Returns:
            Warp information or None if not found

        Raises:
            ValueError: If the index is not initialized or transaction hash is invalid
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # Validate transaction hash
        if not self.validator.validate_transaction_hash(tx_hash):
            raise ValueError(f"Invalid transaction hash: {tx_hash}")
        
        # In a real implementation, this would query the index API
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

        Raises:
            ValueError: If the index is not initialized
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # In a real implementation, this would query the index API
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

    async def search_warps(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Search for Warps by name, title, or description.

        Args:
            query: Search query
            limit: Maximum number of Warps to return
            offset: Offset for pagination

        Returns:
            List of matching Warps

        Raises:
            ValueError: If the index is not initialized
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # Validate parameters
        if not query:
            raise ValueError("Search query cannot be empty")
        
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValueError("Offset must be non-negative")
        
        # In a real implementation, this would query the index API
        # For now, return dummy Warps that match the query
        return [
            {
                "name": f"{query}-warp-{i}",
                "title": f"{query.capitalize()} Warp {i}",
                "description": f"This is a {query} Warp {i}",
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
                    "hash": f"dummy_hash_{query}_{i}",
                    "creator": "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                    "createdAt": f"2023-01-0{i+1}T00:00:00Z"
                }
            }
            for i in range(offset, offset + limit)
        ]

    async def get_brands(
        self,
        limit: int = 10,
        offset: int = 0,
        creator: Optional[str] = None,
        sort: str = "createdAt",
        order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get a list of brands from the index.

        Args:
            limit: Maximum number of brands to return
            offset: Offset for pagination
            creator: Filter by creator address
            sort: Sort field
            order: Sort order (asc or desc)

        Returns:
            List of brands

        Raises:
            ValueError: If the index is not initialized
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # Validate parameters
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValueError("Offset must be non-negative")
        
        if creator and not self.validator.validate_address(creator):
            raise ValueError(f"Invalid creator address: {creator}")
        
        if sort not in ["createdAt", "name"]:
            raise ValueError(f"Invalid sort field: {sort}")
        
        if order not in ["asc", "desc"]:
            raise ValueError(f"Invalid order: {order}")
        
        # In a real implementation, this would query the index API
        # For now, return dummy brands
        return [
            {
                "name": f"example-brand-{i}",
                "description": f"This is example brand {i}",
                "logo": f"https://example.com/logo{i}.png",
                "urls": {
                    "web": f"https://example{i}.com"
                },
                "colors": {
                    "primary": "#FF0000",
                    "secondary": "#00FF00"
                },
                "cta": {
                    "title": "Visit Website",
                    "description": "Visit our website to learn more",
                    "label": "Visit",
                    "url": f"https://example{i}.com"
                },
                "metadata": {
                    "hash": f"dummy_brand_hash_{i}",
                    "creator": creator or "erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                    "createdAt": f"2023-01-0{i+1}T00:00:00Z"
                }
            }
            for i in range(offset, offset + limit)
        ]

    async def get_brand(self, brand_hash: str) -> Optional[Dict[str, Any]]:
        """Get a brand by its hash.

        Args:
            brand_hash: Brand hash

        Returns:
            Brand information or None if not found

        Raises:
            ValueError: If the index is not initialized or brand hash is invalid
        """
        if not self._initialized:
            raise ValueError("Index not initialized. Call init() first.")
        
        # Validate brand hash (same format as transaction hash)
        if not self.validator.validate_transaction_hash(brand_hash):
            raise ValueError(f"Invalid brand hash: {brand_hash}")
        
        # In a real implementation, this would query the index API
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
