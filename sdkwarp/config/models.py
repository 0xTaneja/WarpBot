"""Configuration models for the SDK."""

from enum import Enum
from typing import Optional, Dict, Any, Union

from pydantic import BaseModel, Field


class ChainEnv(str, Enum):
    """Chain environment enum."""
    
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet"


class Config(BaseModel):
    """SDK configuration model."""
    
    # Chain configuration
    env: ChainEnv = Field(default=ChainEnv.DEVNET, description="Chain environment")
    chain_id: Optional[str] = Field(default=None, description="Chain ID")
    chain_api_url: Optional[str] = Field(default=None, description="Chain API URL")
    
    # User configuration
    user_address: Optional[str] = Field(default=None, description="User address")
    
    # Wallet configuration
    wallet_pem_path: Optional[str] = Field(default=None, description="Path to PEM wallet file")
    wallet_keystore_path: Optional[str] = Field(default=None, description="Path to keystore wallet file")
    wallet_password: Optional[str] = Field(default=None, description="Password for keystore wallet")
    wallet_secret_key: Optional[str] = Field(default=None, description="Secret key for wallet")
    
    # Registry configuration
    registry_address: Optional[str] = Field(default=None, description="Registry contract address")
    
    # Cache configuration
    cache_enabled: bool = Field(default=True, description="Enable caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    
    # Additional configuration
    extra_config: Dict[str, Any] = Field(default_factory=dict, description="Additional configuration")
    
    def get_extra(self, key: str, default: Any = None) -> Any:
        """Get extra configuration value."""
        return self.extra_config.get(key, default)
    
    def set_extra(self, key: str, value: Any) -> None:
        """Set extra configuration value."""
        self.extra_config[key] = value
    
    class Config:
        """Pydantic model configuration."""
        
        arbitrary_types_allowed = True
        extra = "allow"


# Transaction data model
class TransactionData(BaseModel):
    """Transaction data model."""
    
    sender: str
    receiver: str
    value: str = "0"
    data: Optional[str] = None
    gas_limit: int = 50000000
    chain_id: str
    version: int = 1
    options: int = 0
    nonce: Optional[int] = None
