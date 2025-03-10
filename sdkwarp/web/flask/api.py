"""Flask API integration for the SDK."""

import json
from typing import Dict, Any, Optional, List, Union, Callable

try:
    from flask import Flask, request, jsonify, Blueprint
except ImportError:
    raise ImportError("Flask is not installed. Install it with 'pip install flask'.")

from sdkwarp.config.models import Config
from sdkwarp.core.registry import Registry, Index
from sdkwarp.core.builder import WarpBuilder, BrandBuilder


class FlaskAPI:
    """Flask API integration for the SDK."""

    def __init__(
        self,
        config: Config,
        registry: Optional[Registry] = None,
        index: Optional[Index] = None,
        blueprint_name: str = "warp",
        url_prefix: str = "/api/warp"
    ):
        """Initialize the Flask API.

        Args:
            config: SDK configuration
            registry: Registry instance
            index: Index instance
            blueprint_name: Blueprint name
            url_prefix: URL prefix for the API
        """
        self.config = config
        self.registry = registry
        self.index = index
        self.blueprint_name = blueprint_name
        self.url_prefix = url_prefix
        self.blueprint = Blueprint(blueprint_name, __name__)
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up API routes."""
        # Warp routes
        self.blueprint.route("/warps", methods=["GET"])(self.get_warps)
        self.blueprint.route("/warps/<tx_hash>", methods=["GET"])(self.get_warp)
        self.blueprint.route("/warps/alias/<alias>", methods=["GET"])(self.get_warp_by_alias)
        self.blueprint.route("/warps/search", methods=["GET"])(self.search_warps)
        
        # Brand routes
        self.blueprint.route("/brands", methods=["GET"])(self.get_brands)
        self.blueprint.route("/brands/<brand_hash>", methods=["GET"])(self.get_brand)
        
        # Registry routes
        self.blueprint.route("/registry/<tx_hash>", methods=["GET"])(self.get_registry_info)
        
        # Builder routes
        self.blueprint.route("/builder/warp", methods=["POST"])(self.build_warp)
        self.blueprint.route("/builder/brand", methods=["POST"])(self.build_brand)

    def register(self, app: Flask) -> None:
        """Register the blueprint with a Flask app.

        Args:
            app: Flask application
        """
        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)

    async def get_warps(self):
        """Get a list of Warps.

        Returns:
            JSON response with Warps
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        # Get query parameters
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)
        creator = request.args.get("creator")
        sort = request.args.get("sort", "createdAt")
        order = request.args.get("order", "desc")
        
        try:
            warps = await self.index.get_warps(
                limit=limit,
                offset=offset,
                creator=creator,
                sort=sort,
                order=order
            )
            return jsonify({"warps": warps, "count": len(warps)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def get_warp(self, tx_hash: str):
        """Get a Warp by its transaction hash.

        Args:
            tx_hash: Transaction hash

        Returns:
            JSON response with Warp
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        try:
            warp = await self.index.get_warp(tx_hash)
            if not warp:
                return jsonify({"error": "Warp not found"}), 404
            
            return jsonify(warp)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def get_warp_by_alias(self, alias: str):
        """Get a Warp by its alias.

        Args:
            alias: Warp alias

        Returns:
            JSON response with Warp
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        try:
            warp = await self.index.get_warp_by_alias(alias)
            if not warp:
                return jsonify({"error": "Warp not found"}), 404
            
            return jsonify(warp)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def search_warps(self):
        """Search for Warps.

        Returns:
            JSON response with matching Warps
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        # Get query parameters
        query = request.args.get("q")
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)
        
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        try:
            warps = await self.index.search_warps(
                query=query,
                limit=limit,
                offset=offset
            )
            return jsonify({"warps": warps, "count": len(warps)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def get_brands(self):
        """Get a list of brands.

        Returns:
            JSON response with brands
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        # Get query parameters
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)
        creator = request.args.get("creator")
        sort = request.args.get("sort", "createdAt")
        order = request.args.get("order", "desc")
        
        try:
            brands = await self.index.get_brands(
                limit=limit,
                offset=offset,
                creator=creator,
                sort=sort,
                order=order
            )
            return jsonify({"brands": brands, "count": len(brands)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def get_brand(self, brand_hash: str):
        """Get a brand by its hash.

        Args:
            brand_hash: Brand hash

        Returns:
            JSON response with brand
        """
        if not self.index:
            return jsonify({"error": "Index not initialized"}), 500
        
        try:
            brand = await self.index.get_brand(brand_hash)
            if not brand:
                return jsonify({"error": "Brand not found"}), 404
            
            return jsonify(brand)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def get_registry_info(self, tx_hash: str):
        """Get registry information for a Warp.

        Args:
            tx_hash: Transaction hash

        Returns:
            JSON response with registry information
        """
        if not self.registry:
            return jsonify({"error": "Registry not initialized"}), 500
        
        try:
            info = await self.registry.get_registry_info(tx_hash)
            if not info:
                return jsonify({"error": "Registry information not found"}), 404
            
            return jsonify(info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def build_warp(self):
        """Build a Warp from request data.

        Returns:
            JSON response with built Warp
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            builder = WarpBuilder(config=self.config)
            
            # Set basic properties
            if "name" in data:
                builder.name(data["name"])
            
            if "title" in data:
                builder.title(data["title"])
            
            if "description" in data:
                builder.description(data["description"])
            
            # Set action properties
            action = data.get("action", {})
            
            if "type" in action:
                builder.action_type(action["type"])
            
            if "title" in action:
                builder.action_title(action["title"])
            
            if "description" in action:
                builder.action_description(action["description"])
            
            if "data" in action:
                builder.action_data(action["data"])
            
            # Set metadata properties
            metadata = data.get("metadata", {})
            
            if "creator" in metadata:
                builder.creator(metadata["creator"])
            
            if "createdAt" in metadata:
                builder.created_at(metadata["createdAt"])
            
            # Build the Warp
            warp = builder.build()
            
            return jsonify(warp)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def build_brand(self):
        """Build a brand from request data.

        Returns:
            JSON response with built brand
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            builder = BrandBuilder(config=self.config)
            
            # Set basic properties
            if "name" in data:
                builder.name(data["name"])
            
            if "description" in data:
                builder.description(data["description"])
            
            if "logo" in data:
                builder.logo(data["logo"])
            
            # Set URLs
            if "urls" in data and isinstance(data["urls"], dict):
                builder.set_urls(data["urls"])
            
            # Set colors
            if "colors" in data and isinstance(data["colors"], dict):
                builder.set_colors(data["colors"])
            
            # Set CTA
            cta = data.get("cta", {})
            if isinstance(cta, dict):
                if "title" in cta:
                    builder.cta_title(cta["title"])
                
                if "description" in cta:
                    builder.cta_description(cta["description"])
                
                if "label" in cta:
                    builder.cta_label(cta["label"])
                
                if "url" in cta:
                    builder.cta_url(cta["url"])
            
            # Set metadata properties
            metadata = data.get("metadata", {})
            
            if "creator" in metadata:
                builder.creator(metadata["creator"])
            
            if "createdAt" in metadata:
                builder.created_at(metadata["createdAt"])
            
            # Build the brand
            brand = builder.build()
            
            return jsonify(brand)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


def create_flask_api(
    config: Config,
    registry: Optional[Registry] = None,
    index: Optional[Index] = None,
    blueprint_name: str = "warp",
    url_prefix: str = "/api/warp"
) -> FlaskAPI:
    """Create a Flask API integration instance.

    Args:
        config: SDK configuration
        registry: Registry instance
        index: Index instance
        blueprint_name: Blueprint name
        url_prefix: URL prefix

    Returns:
        FlaskAPI instance
    """
    return FlaskAPI(
        config=config,
        registry=registry,
        index=index,
        blueprint_name=blueprint_name,
        url_prefix=url_prefix
    )
