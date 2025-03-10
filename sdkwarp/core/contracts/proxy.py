"""Proxy module for interacting with smart contracts."""

import json
import aiohttp
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config
from sdkwarp.core.contracts.loader import ContractLoader
from sdkwarp.core.contracts.cache import Cache
from sdkwarp.core.transaction.transaction import Transaction
from sdkwarp.core.transaction.arg_serializer import ArgSerializer
from sdkwarp.utils.validation import Validator


class Proxy:
    """Proxy for interacting with smart contracts."""

    def __init__(
        self,
        config: Config,
        contract_address: str,
        contract_loader: Optional[ContractLoader] = None,
        cache: Optional[Cache] = None,
        validator: Optional[Validator] = None
    ):
        """Initialize the contract proxy.

        Args:
            config: SDK configuration
            contract_address: Contract address
            contract_loader: Contract loader instance
            cache: Cache instance
            validator: Validator instance
        """
        self.config = config
        self.contract_address = contract_address
        self.contract_loader = contract_loader
        self.cache = cache
        self.validator = validator or Validator()
        self._initialized = False
        self._abi = None

    async def init(self) -> None:
        """Initialize the contract proxy.

        Loads the contract ABI if a contract loader is provided.
        """
        # Validate contract address
        if not self.validator.validate_address(self.contract_address):
            raise ValueError(f"Invalid contract address: {self.contract_address}")
        
        # Load ABI if contract loader is provided
        if self.contract_loader:
            self._abi = await self.contract_loader.load_abi(self.contract_address)
        
        self._initialized = True

    async def call(
        self,
        function: str,
        args: Optional[List[Any]] = None,
        value: str = "0"
    ) -> Transaction:
        """Create a transaction to call a contract function.

        Args:
            function: Function name
            args: Function arguments
            value: Value to send with the call

        Returns:
            Transaction object

        Raises:
            ValueError: If the proxy is not initialized or user address is not set
        """
        if not self._initialized:
            raise ValueError("Contract proxy not initialized. Call init() first.")
        
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Serialize function call
        data = ArgSerializer.serialize_function_call(function, args)
        
        # Create transaction
        return Transaction(
            sender=self.config.user_address,
            receiver=self.contract_address,
            value=value,
            data=data,
            gas_limit=10000000,  # Default gas limit for contract calls
            chain_id=self.config.chain_id or "D"
        )

    async def query(
        self,
        function: str,
        args: Optional[List[Any]] = None,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None
    ) -> Any:
        """Query a contract function.

        Args:
            function: Function name
            args: Function arguments
            use_cache: Whether to use cache
            cache_ttl: Cache TTL in seconds

        Returns:
            Query result

        Raises:
            ValueError: If the proxy is not initialized or chain API URL is not set
        """
        if not self._initialized:
            raise ValueError("Contract proxy not initialized. Call init() first.")
        
        if not self.config.chain_api_url:
            raise ValueError("Chain API URL not set in configuration")
        
        # Generate cache key if using cache
        cache_key = None
        if use_cache and self.cache:
            cache_key = f"query_{self.contract_address}_{function}_{json.dumps(args or [])}"
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Serialize function call
        data = ArgSerializer.serialize_function_call(function, args)
        
        # Prepare query data
        query_data = {
            "scAddress": self.contract_address,
            "funcName": function,
            "args": args or []
        }
        
        # Execute query
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.chain_api_url}/vm-values/query",
                    json=query_data
                ) as response:
                    if response.status != 200:
                        raise ValueError(f"Query failed with status {response.status}")
                    
                    result = await response.json()
                    
                    # Process result
                    # Note: This is a simplified example, actual API response format may differ
                    if "returnData" in result:
                        processed_result = self._process_query_result(result)
                        
                        # Cache result if using cache
                        if use_cache and self.cache and cache_key:
                            self.cache.set(cache_key, processed_result, cache_ttl)
                        
                        return processed_result
                    
                    raise ValueError("Invalid query response format")
        except Exception as e:
            raise ValueError(f"Query failed: {e}")

    def _process_query_result(self, result: Dict[str, Any]) -> Any:
        """Process a query result.

        Args:
            result: Raw query result

        Returns:
            Processed result
        """
        # In a real implementation, this would process the result based on the ABI
        # For now, return a simplified result
        if "returnData" in result:
            return {
                "returnData": result["returnData"],
                "gasRemaining": result.get("gasRemaining", 0),
                "gasUsed": result.get("gasUsed", 0),
                "returnCode": result.get("returnCode", "ok")
            }
        
        return result

    async def get_contract_balance(self) -> Dict[str, Any]:
        """Get the contract's balance.

        Returns:
            Contract balance information

        Raises:
            ValueError: If the proxy is not initialized or chain API URL is not set
        """
        if not self._initialized:
            raise ValueError("Contract proxy not initialized. Call init() first.")
        
        if not self.config.chain_api_url:
            raise ValueError("Chain API URL not set in configuration")
        
        # Generate cache key if using cache
        cache_key = f"balance_{self.contract_address}"
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Fetch balance
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.chain_api_url}/address/{self.contract_address}/balance"
                ) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to get balance with status {response.status}")
                    
                    result = await response.json()
                    
                    # Cache result
                    if self.cache:
                        self.cache.set(cache_key, result)
                    
                    return result
        except Exception as e:
            raise ValueError(f"Failed to get balance: {e}")

    async def get_contract_storage(
        self,
        key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the contract's storage.

        Args:
            key: Optional storage key

        Returns:
            Contract storage information

        Raises:
            ValueError: If the proxy is not initialized or chain API URL is not set
        """
        if not self._initialized:
            raise ValueError("Contract proxy not initialized. Call init() first.")
        
        if not self.config.chain_api_url:
            raise ValueError("Chain API URL not set in configuration")
        
        # Generate cache key if using cache
        cache_key = f"storage_{self.contract_address}_{key or 'all'}"
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Fetch storage
        try:
            url = f"{self.config.chain_api_url}/address/{self.contract_address}/storage"
            if key:
                url += f"/{key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to get storage with status {response.status}")
                    
                    result = await response.json()
                    
                    # Cache result
                    if self.cache:
                        self.cache.set(cache_key, result)
                    
                    return result
        except Exception as e:
            raise ValueError(f"Failed to get storage: {e}")

    def get_abi(self) -> Optional[Dict[str, Any]]:
        """Get the contract ABI.

        Returns:
            Contract ABI or None if not loaded
        """
        return self._abi
