"""Web framework integrations for the SDK."""

# Import Flask integration if available
try:
    from sdkwarp.web.flask.api import FlaskAPI, create_flask_api
except ImportError:
    # Flask is not installed
    pass

# Import FastAPI integration if available
try:
    from sdkwarp.web.fastapi.api import FastAPI, create_fastapi_api
except ImportError:
    # FastAPI is not installed
    pass

__all__ = [
    # Flask integration
    "FlaskAPI",
    "create_flask_api",
    
    # FastAPI integration
    "FastAPI",
    "create_fastapi_api"
]
