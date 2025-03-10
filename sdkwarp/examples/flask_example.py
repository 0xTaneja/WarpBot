"""Example of using the Flask integration."""

import asyncio
from flask import Flask

from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.core.registry import Registry, Index
from sdkwarp.web.flask import create_flask_api


async def setup_api():
    """Set up the API."""
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
    
    # Create Flask integration
    api = create_flask_api(
        config=config,
        registry=registry,
        index=index
    )
    
    return api


def create_app():
    """Create the Flask app."""
    # Create a Flask app
    app = Flask(__name__)
    
    # Set up the API
    api = asyncio.run(setup_api())
    
    # Register the API with the Flask app
    api.register_blueprint(app)
    
    return app


if __name__ == "__main__":
    # Create the app
    app = create_app()
    
    # Run the app
    app.run(host="0.0.0.0", port=5000, debug=True) 