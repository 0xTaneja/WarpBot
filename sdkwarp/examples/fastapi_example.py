"""Example of using the FastAPI integration."""

import asyncio
import uvicorn
from fastapi import FastAPI

from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.core.registry import Registry, Index
from sdkwarp.web.fastapi import create_fastapi_api


async def main():
    """Run the example."""
    # Create a FastAPI app
    app = FastAPI(title="Warp SDK API", description="API for the Warp SDK")
    
    # Create SDK configuration
    config = Config(
        env=ChainEnv.DEVNET,
        chain_id="D",
        chain_api_url="https://devnet-api.multiversx.com",
        user_address="erd1...",  # Replace with your address
        registry_address="erd1..."  # Replace with registry address
    )
    
    # Create Registry and Index instances
    registry = Registry(config=config)
    index = Index(config=config, registry=registry)
    
    # Initialize Registry and Index
    await registry.init()
    await index.init()
    
    # Create FastAPI integration
    api = create_fastapi_api(
        config=config,
        registry=registry,
        index=index
    )
    
    # Register the API with the FastAPI app
    api.register(app)
    
    # Return the app for running
    return app


if __name__ == "__main__":
    # Create the app
    app = asyncio.run(main())
    
    # Run the app
    uvicorn.run(app, host="0.0.0.0", port=8000) 