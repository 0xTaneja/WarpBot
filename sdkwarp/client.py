"""Main client for the SDK providing unified access to all SDK components."""

import logging
import os
from typing import Any, Dict, Optional, Union

from sdkwarp.config.loader import get_config
from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.core.builder.warp_builder import WarpBuilder
from sdkwarp.core.builder.brand_builder import BrandBuilder
from sdkwarp.core.registry.registry import Registry
from sdkwarp.core.registry.index import Index
from sdkwarp.core.transaction.signer import Signer
from sdkwarp.core.transaction.executor import ActionExecutor
from sdkwarp.core.transaction.serializer import ArgSerializer
from sdkwarp.core.contracts.loader import ContractLoader
from sdkwarp.core.contracts.cache import Cache
from sdkwarp.core.contracts.proxy import Proxy
from sdkwarp.utils.validation import Validator


class Client:
    """Unified client for the SDK.
    
    This client provides access to all SDK components with a unified interface.
    It handles configuration and initialization of components.
    """
    
    def __init__(
        self,
        env: Optional[Union[str, ChainEnv]] = None,
        user_address: Optional[str] = None,
        chain_api_url: Optional[str] = None,
        config_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        **kwargs
    ):
        """Initialize the client.
        
        Args:
            env: Chain environment (devnet, testnet, mainnet)
            user_address: User address
            chain_api_url: Chain API URL
            config_path: Path to configuration file
            logger: Logger instance
            **kwargs: Additional configuration parameters
        """
        self.logger = logger or logging.getLogger("sdkwarp")
        
        # Load configuration
        self.config = get_config(
            env=env,
            user_address=user_address,
            chain_api_url=chain_api_url,
            config_path=config_path,
            **kwargs
        )
        
        # Initialize components
        self._init_components()
    
    def _init_components(self) -> None:
        """Initialize SDK components."""
        # Core components
        self.cache = Cache(self.config)
        self.contract_loader = ContractLoader(self.config, self.cache)
        
        # Builder components
        self.builder = WarpBuilder(self.config)
        self.brand_builder = BrandBuilder(self.config)
        
        # Registry components
        self.registry = Registry(self.config, self.contract_loader)
        self.index = Index(self.config)
        
        # Transaction components
        self.signer = Signer(self.config)
        self.executor = ActionExecutor(self.config, self.contract_loader)
        self.serializer = ArgSerializer(self.config)
        
        # Proxy component
        self.proxy = Proxy(self.config, self.contract_loader)
        
        # Validator component
        self.validator = Validator(self.config)
    
    async def init(self) -> None:
        """Initialize async components.
        
        This method should be called before using async components.
        """
        await self.registry.init()
        await self.index.init()
        await self.executor.init()
    
    def load_wallet_pem(self, pem_path: str) -> None:
        """Load wallet from PEM file.
        
        Args:
            pem_path: Path to PEM file
        """
        self.config.wallet_pem_path = pem_path
        self.signer.load_wallet_pem(pem_path)
    
    def load_wallet_keystore(self, keystore_path: str, password: str) -> None:
        """Load wallet from keystore file.
        
        Args:
            keystore_path: Path to keystore file
            password: Keystore password
        """
        self.config.wallet_keystore_path = keystore_path
        self.config.wallet_password = password
        self.signer.load_wallet_keystore(keystore_path, password)
    
    def load_wallet_secret_key(self, secret_key: str) -> None:
        """Load wallet from secret key.
        
        Args:
            secret_key: Hex-encoded private key
        """
        self.config.wallet_secret_key = secret_key
        self.signer.load_wallet_secret_key(secret_key)


def create_client(
    env: Optional[Union[str, ChainEnv]] = None,
    user_address: Optional[str] = None,
    chain_api_url: Optional[str] = None,
    config_path: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    **kwargs
) -> Client:
    """Create a client instance.
    
    Args:
        env: Chain environment (devnet, testnet, mainnet)
        user_address: User address
        chain_api_url: Chain API URL
        config_path: Path to configuration file
        logger: Logger instance
        **kwargs: Additional configuration parameters
    
    Returns:
        Client instance
    """
    return Client(
        env=env,
        user_address=user_address,
        chain_api_url=chain_api_url,
        config_path=config_path,
        logger=logger,
        **kwargs
    )


def create_client_from_env(
    logger: Optional[logging.Logger] = None
) -> Client:
    """Create a client instance from environment variables.
    
    Args:
        logger: Logger instance
    
    Returns:
        Client instance
    """
    return Client(logger=logger)
