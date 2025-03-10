"""MultiversX Warp SDK for Python - Refactored Version."""

from sdkwarp.client import (
    Client,
    create_client,
    create_client_from_env
)

# Import core types and components
from sdkwarp.config.models import Config, ChainEnv, TransactionData

# Import builder components
from sdkwarp.core.builder.warp_builder import WarpBuilder
from sdkwarp.core.builder.brand_builder import BrandBuilder

# Import registry components
from sdkwarp.core.registry.registry import Registry
from sdkwarp.core.registry.index import Index

# Import transaction components
from sdkwarp.core.transaction.signer import Signer
from sdkwarp.core.transaction.executor import ActionExecutor
from sdkwarp.core.transaction.serializer import ArgSerializer

# Import contract components
from sdkwarp.core.contracts.loader import ContractLoader
from sdkwarp.core.contracts.cache import Cache
from sdkwarp.core.contracts.proxy import Proxy

# Import utility components
from sdkwarp.utils.codec import Codec
from sdkwarp.utils.validation import Validator

# Import web integrations if available
try:
    from sdkwarp.web.flask import FlaskAPI, create_flask_api
except ImportError:
    # Flask is not installed
    pass

try:
    from sdkwarp.web.fastapi import FastAPI, create_fastapi_api
except ImportError:
    # FastAPI is not installed
    pass

__version__ = "0.1.0"

__all__ = [
    # Client
    "Client",
    "create_client",
    "create_client_from_env",
    
    # Configuration
    "Config",
    "ChainEnv",
    "TransactionData",
    
    # Builder components
    "WarpBuilder",
    "BrandBuilder",
    
    # Registry components
    "Registry",
    "Index",
    
    # Transaction components
    "Signer",
    "ActionExecutor",
    "ArgSerializer",
    
    # Contract components
    "ContractLoader",
    "Cache",
    "Proxy",
    
    # Utility components
    "Codec",
    "Validator",
    
    # Web integrations
    "FlaskAPI",
    "create_flask_api",
    "FastAPI",
    "create_fastapi_api",
    
    # Version
    "__version__"
]
