# SDKWarp - MultiversX Warp SDK for Python

A comprehensive Python SDK for creating, managing, and interacting with [MultiversX Warps](https://docs.multiversx.com/sdk-and-tools/sdk-py/), with an improved and refactored codebase.

## Features

- **Full Warp Protocol Support**: Create, register, upgrade, and query Warps on the MultiversX blockchain
- **Dynamic Configuration**: Load configuration from environment variables, config files, or code
- **Flexible API Design**: Use the unified client or individual components based on your needs
- **Transaction Signing**: Sign transactions with PEM, keystore, or private key wallets
- **Strong Type Safety**: Built with Pydantic for data validation and type checking
- **Async/Await Pattern**: Modern asynchronous API for efficient blockchain interactions
- **Web Framework Integrations**: Ready-to-use integrations for Flask and FastAPI
- **Improved Code Organization**: Logically structured modules with reduced duplication

## Installation

```bash
# Using pip (basic installation)
pip install sdkwarp

# With web framework integrations
pip install sdkwarp[web]  # Installs both Flask and FastAPI integrations
pip install sdkwarp[flask]  # Only Flask integration
pip install sdkwarp[fastapi]  # Only FastAPI integration

# Using Poetry
poetry add sdkwarp
poetry add sdkwarp -E web  # With web integrations
```

## Quick Start

### Using the Dynamic Client (Recommended)

The `Client` provides a unified interface to all SDK components with dynamic configuration:

```python
import asyncio
from sdkwarp import Client

async def main():
    # Create a client with automatic configuration
    client = Client(
        env="testnet",
        user_address="erd1..."
    )
    
    # Create a Warp
    warp = client.builder.name("my-warp")\
        .title("My First Warp")\
        .description("A simple EGLD transfer Warp")\
        .action_transfer(
            title="Send EGLD",
            description="Send some EGLD to an address"
        )\
        .build()
    
    # Create a transaction
    tx = client.builder.create_inscription_transaction(warp)
    print(f"Transaction created with gas limit: {tx.gas_limit}")
    
    # After sending the transaction and obtaining the hash, you can register it
    await client.init()  # Initialize async components
    tx_hash = "your-transaction-hash"
    register_tx = client.registry.create_warp_register_transaction(tx_hash)

if __name__ == "__main__":
    asyncio.run(main())
```

### Web Framework Integrations

The SDK provides integrations for Flask and FastAPI:

#### Flask Integration

```python
import asyncio
from flask import Flask
from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.core.registry import Registry, Index
from sdkwarp.web.flask import create_flask_api

# Create a Flask app
app = Flask(__name__)

# Create and set up the API
config = Config(env=ChainEnv.DEVNET, chain_id="D")
registry = Registry(config=config)
index = Index(config=config, registry=registry)

# Initialize components and register with Flask
asyncio.run(registry.init())
asyncio.run(index.init())
api = create_flask_api(config=config, registry=registry, index=index)
api.register_blueprint(app)

# Run the app
app.run(host="0.0.0.0", port=5000)
```

#### FastAPI Integration

```python
import asyncio
import uvicorn
from fastapi import FastAPI
from sdkwarp.config.models import Config, ChainEnv
from sdkwarp.core.registry import Registry, Index
from sdkwarp.web.fastapi import create_fastapi_api

# Create a FastAPI app
app = FastAPI(title="Warp SDK API")

# Create and set up the API
config = Config(env=ChainEnv.DEVNET, chain_id="D")
registry = Registry(config=config)
index = Index(config=config, registry=registry)

# Initialize components and register with FastAPI
asyncio.run(registry.init())
asyncio.run(index.init())
api = create_fastapi_api(config=config, registry=registry, index=index)
api.register(app)

# Run the app
uvicorn.run(app, host="0.0.0.0", port=8000)
```

For more detailed examples, see the [examples directory](sdkwarp/examples/).

## Project Structure

The SDK follows a clean, modular structure:

```
sdkwarp/
├── config/           # All configuration-related code
│   ├── loader.py     # Configuration loading logic
│   ├── models.py     # Pydantic models for configuration
│   └── constants.py  # Environment-specific constants
├── utils/            # Utility functions
│   ├── codec.py      # Encoding/decoding utilities
│   ├── validation.py # Validation helpers
│   ├── formatting.py # String formatting utilities
│   └── helpers.py    # General purpose helpers
├── core/             # Core functionality
│   ├── builder/      # Warp building components
│   ├── registry/     # Registry interaction
│   ├── transaction/  # Transaction handling
│   └── contracts/    # Contract interaction
├── web/              # Web framework integrations
│   ├── flask/        # Flask integration
│   └── fastapi/      # FastAPI integration
├── examples/         # Example implementations
│   ├── flask_example.py    # Flask integration example
│   └── fastapi_example.py  # FastAPI integration example
├── client.py         # Main client interface
└── cli.py            # Command-line interface
```

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/yourusername/sdkwarp.git
cd sdkwarp

# Install dependencies with development extras
pip install -e ".[dev,web]"

# Or using Poetry
poetry install -E dev -E web

# Run tests
pytest

# Run examples
python -m sdkwarp.examples.flask_example
python -m sdkwarp.examples.fastapi_example
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 