"""Contract loader module for loading smart contract ABIs."""

import json
import os
import aiohttp
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config
from sdkwarp.utils.validation import Validator


class ContractLoader:
    """Contract loader for loading smart contract ABIs."""

    def __init__(
        self,
        config: Config,
        validator: Optional[Validator] = None
    ):
        """Initialize the contract loader.

        Args:
            config: SDK configuration
            validator: Validator instance
        """
        self.config = config
        self.validator = validator or Validator()
        self._initialized = False
        self._abi_cache = {}

    async def init(self) -> None:
        """Initialize the contract loader."""
        self._initialized = True

    async def load_abi(
        self,
        contract_address: str,
        force_reload: bool = False
    ) -> Dict[str, Any]:
        """Load ABI for a contract.

        Args:
            contract_address: Contract address
            force_reload: Force reload from source

        Returns:
            Contract ABI

        Raises:
            ValueError: If the contract loader is not initialized or contract address is invalid
        """
        if not self._initialized:
            raise ValueError("Contract loader not initialized. Call init() first.")
        
        # Validate contract address
        if not self.validator.validate_address(contract_address):
            raise ValueError(f"Invalid contract address: {contract_address}")
        
        # Check cache first if not forcing reload
        if not force_reload and contract_address in self._abi_cache:
            return self._abi_cache[contract_address]
        
        # Try to load from local file first
        abi = await self._load_abi_from_file(contract_address)
        
        # If not found locally, try to load from API
        if not abi:
            abi = await self._load_abi_from_api(contract_address)
        
        # Cache the ABI
        if abi:
            self._abi_cache[contract_address] = abi
        
        return abi or {}

    async def _load_abi_from_file(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Load ABI from a local file.

        Args:
            contract_address: Contract address

        Returns:
            Contract ABI or None if not found
        """
        # Check if ABI directory is configured
        if not self.config.abi_directory:
            return None
        
        # Construct file path
        file_path = os.path.join(self.config.abi_directory, f"{contract_address}.json")
        
        # Check if file exists
        if not os.path.isfile(file_path):
            return None
        
        try:
            # Read and parse the file
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            # Log error and return None
            print(f"Error loading ABI from file: {e}")
            return None

    async def _load_abi_from_api(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Load ABI from the API.

        Args:
            contract_address: Contract address

        Returns:
            Contract ABI or None if not found
        """
        # Check if API URL is configured
        if not self.config.chain_api_url:
            return None
        
        # Construct API URL
        api_url = f"{self.config.chain_api_url}/address/{contract_address}/esdt"
        
        try:
            # Fetch ABI from API
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.json()
                    
                    # Extract ABI from response
                    # Note: This is a simplified example, actual API response format may differ
                    if "abi" in data:
                        return data["abi"]
                    
                    return None
        except Exception as e:
            # Log error and return None
            print(f"Error loading ABI from API: {e}")
            return None

    async def save_abi(self, contract_address: str, abi: Dict[str, Any]) -> bool:
        """Save ABI to a local file.

        Args:
            contract_address: Contract address
            abi: Contract ABI

        Returns:
            True if saved successfully, False otherwise

        Raises:
            ValueError: If the contract loader is not initialized or contract address is invalid
        """
        if not self._initialized:
            raise ValueError("Contract loader not initialized. Call init() first.")
        
        # Validate contract address
        if not self.validator.validate_address(contract_address):
            raise ValueError(f"Invalid contract address: {contract_address}")
        
        # Check if ABI directory is configured
        if not self.config.abi_directory:
            return False
        
        # Ensure directory exists
        os.makedirs(self.config.abi_directory, exist_ok=True)
        
        # Construct file path
        file_path = os.path.join(self.config.abi_directory, f"{contract_address}.json")
        
        try:
            # Write ABI to file
            with open(file_path, "w") as f:
                json.dump(abi, f, indent=2)
            
            # Update cache
            self._abi_cache[contract_address] = abi
            
            return True
        except Exception as e:
            # Log error and return False
            print(f"Error saving ABI to file: {e}")
            return False

    def get_cached_abi(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Get ABI from cache.

        Args:
            contract_address: Contract address

        Returns:
            Contract ABI or None if not in cache
        """
        return self._abi_cache.get(contract_address)

    def clear_cache(self) -> None:
        """Clear the ABI cache."""
        self._abi_cache = {}
