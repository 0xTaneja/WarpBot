# SDK Examples

This directory contains examples of how to use the SDK.

## Web Framework Integrations

### Flask Integration

The `flask_example.py` file demonstrates how to use the Flask integration.

To run the example:

1. Install the required dependencies:
   ```bash
   pip install flask
   ```

2. Update the example with your configuration:
   - Replace `"erd1..."` with your address
   - Replace `"erd1..."` with the registry address

3. Run the example:
   ```bash
   # From the root of the sdkwarp package
   python -m sdkwarp.examples.flask_example
   ```

4. Access the API at http://localhost:5000/api/warp

### FastAPI Integration

The `fastapi_example.py` file demonstrates how to use the FastAPI integration.

To run the example:

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Update the example with your configuration:
   - Replace `"erd1..."` with your address
   - Replace `"erd1..."` with the registry address

3. Run the example:
   ```bash
   # From the root of the sdkwarp package
   python -m sdkwarp.examples.fastapi_example
   ```

4. Access the API at http://localhost:8000/api/warp

5. Access the Swagger UI at http://localhost:8000/docs

## API Endpoints

Both Flask and FastAPI integrations provide the following endpoints:

### Warps

- `GET /api/warp/warps` - Get a list of Warps
- `GET /api/warp/warps/{tx_hash}` - Get a Warp by its transaction hash
- `GET /api/warp/warps/alias/{alias}` - Get a Warp by its alias
- `GET /api/warp/warps/search?q={query}` - Search for Warps
- `POST /api/warp/builder/warp` - Build a Warp

### Brands

- `GET /api/warp/brands` - Get a list of brands
- `GET /api/warp/brands/{brand_hash}` - Get a brand by its hash
- `POST /api/warp/builder/brand` - Build a brand

### Registry

- `GET /api/warp/registry/{tx_hash}` - Get registry information for a Warp 