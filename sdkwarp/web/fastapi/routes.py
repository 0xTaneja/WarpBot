"""Route definitions for FastAPI integration."""

from typing import Dict, Any, Optional, List, Union, Callable

try:
    from fastapi import APIRouter, Query, Path, Body, HTTPException, Depends
    from pydantic import BaseModel, Field
except ImportError:
    raise ImportError("FastAPI is not installed. Install it with 'pip install fastapi'.")

from sdkwarp.config.models import Config
from sdkwarp.core.registry import Registry, Index
from sdkwarp.core.builder import WarpBuilder, BrandBuilder


class WarpRoutes:
    """Warp routes for FastAPI."""

    def __init__(
        self,
        config: Config,
        registry: Optional[Registry] = None,
        index: Optional[Index] = None,
        prefix: str = "/warps"
    ):
        """Initialize Warp routes.

        Args:
            config: SDK configuration
            registry: Registry instance
            index: Index instance
            prefix: Route prefix
        """
        self.config = config
        self.registry = registry
        self.index = index
        self.router = APIRouter(prefix=prefix)
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up routes."""
        self.router.add_api_route(
            "",
            self.get_warps,
            methods=["GET"],
            summary="Get Warps",
            description="Get a list of Warps with pagination and filtering options."
        )
        
        self.router.add_api_route(
            "/{tx_hash}",
            self.get_warp,
            methods=["GET"],
            summary="Get Warp",
            description="Get a Warp by its transaction hash."
        )
        
        self.router.add_api_route(
            "/alias/{alias}",
            self.get_warp_by_alias,
            methods=["GET"],
            summary="Get Warp by Alias",
            description="Get a Warp by its alias."
        )
        
        self.router.add_api_route(
            "/search",
            self.search_warps,
            methods=["GET"],
            summary="Search Warps",
            description="Search for Warps by name, title, or description."
        )
        
        self.router.add_api_route(
            "/build",
            self.build_warp,
            methods=["POST"],
            summary="Build Warp",
            description="Build a Warp from request data."
        )

    async def get_warps(
        self,
        limit: int = Query(10, ge=1, le=100, description="Maximum number of Warps to return"),
        offset: int = Query(0, ge=0, description="Offset for pagination"),
        creator: Optional[str] = Query(None, description="Filter by creator address"),
        sort: str = Query("createdAt", description="Sort field"),
        order: str = Query("desc", description="Sort order (asc or desc)")
    ) -> Dict[str, Any]:
        """Get a list of Warps.

        Args:
            limit: Maximum number of Warps to return
            offset: Offset for pagination
            creator: Filter by creator address
            sort: Sort field
            order: Sort order (asc or desc)

        Returns:
            List of Warps and count

        Raises:
            HTTPException: If the index is not initialized or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            warps = await self.index.get_warps(
                limit=limit,
                offset=offset,
                creator=creator,
                sort=sort,
                order=order
            )
            return {"warps": warps, "count": len(warps)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_warp(
        self,
        tx_hash: str = Path(..., description="Transaction hash of the Warp")
    ) -> Dict[str, Any]:
        """Get a Warp by its transaction hash.

        Args:
            tx_hash: Transaction hash

        Returns:
            Warp information

        Raises:
            HTTPException: If the index is not initialized, Warp is not found, or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            warp = await self.index.get_warp(tx_hash)
            if not warp:
                raise HTTPException(status_code=404, detail="Warp not found")
            
            return warp
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_warp_by_alias(
        self,
        alias: str = Path(..., description="Warp alias")
    ) -> Dict[str, Any]:
        """Get a Warp by its alias.

        Args:
            alias: Warp alias

        Returns:
            Warp information

        Raises:
            HTTPException: If the index is not initialized, Warp is not found, or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            warp = await self.index.get_warp_by_alias(alias)
            if not warp:
                raise HTTPException(status_code=404, detail="Warp not found")
            
            return warp
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_warps(
        self,
        q: str = Query(..., description="Search query"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of Warps to return"),
        offset: int = Query(0, ge=0, description="Offset for pagination")
    ) -> Dict[str, Any]:
        """Search for Warps.

        Args:
            q: Search query
            limit: Maximum number of Warps to return
            offset: Offset for pagination

        Returns:
            List of matching Warps and count

        Raises:
            HTTPException: If the index is not initialized or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            warps = await self.index.search_warps(
                query=q,
                limit=limit,
                offset=offset
            )
            return {"warps": warps, "count": len(warps)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def build_warp(
        self,
        warp_data: Dict[str, Any] = Body(..., description="Warp data")
    ) -> Dict[str, Any]:
        """Build a Warp from request data.

        Args:
            warp_data: Warp data

        Returns:
            Built Warp

        Raises:
            HTTPException: If an error occurs during building
        """
        try:
            builder = WarpBuilder(config=self.config)
            
            # Set basic properties
            if "name" in warp_data:
                builder.name(warp_data["name"])
            
            if "title" in warp_data:
                builder.title(warp_data["title"])
            
            if "description" in warp_data:
                builder.description(warp_data["description"])
            
            # Set action properties
            if "action" in warp_data:
                action = warp_data["action"]
                
                if "type" in action:
                    builder.action_type(action["type"])
                
                if "title" in action:
                    builder.action_title(action["title"])
                
                if "description" in action:
                    builder.action_description(action["description"])
                
                if "data" in action:
                    builder.action_data(action["data"])
            
            # Set metadata properties
            if "metadata" in warp_data:
                metadata = warp_data["metadata"]
                
                if "creator" in metadata:
                    builder.creator(metadata["creator"])
                
                if "createdAt" in metadata:
                    builder.created_at(metadata["createdAt"])
            
            # Build the Warp
            built_warp = builder.build()
            
            return built_warp
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class BrandRoutes:
    """Brand routes for FastAPI."""

    def __init__(
        self,
        config: Config,
        registry: Optional[Registry] = None,
        index: Optional[Index] = None,
        prefix: str = "/brands"
    ):
        """Initialize Brand routes.

        Args:
            config: SDK configuration
            registry: Registry instance
            index: Index instance
            prefix: Route prefix
        """
        self.config = config
        self.registry = registry
        self.index = index
        self.router = APIRouter(prefix=prefix)
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up routes."""
        self.router.add_api_route(
            "",
            self.get_brands,
            methods=["GET"],
            summary="Get Brands",
            description="Get a list of brands with pagination and filtering options."
        )
        
        self.router.add_api_route(
            "/{brand_hash}",
            self.get_brand,
            methods=["GET"],
            summary="Get Brand",
            description="Get a brand by its hash."
        )
        
        self.router.add_api_route(
            "/build",
            self.build_brand,
            methods=["POST"],
            summary="Build Brand",
            description="Build a brand from request data."
        )

    async def get_brands(
        self,
        limit: int = Query(10, ge=1, le=100, description="Maximum number of brands to return"),
        offset: int = Query(0, ge=0, description="Offset for pagination"),
        creator: Optional[str] = Query(None, description="Filter by creator address"),
        sort: str = Query("createdAt", description="Sort field"),
        order: str = Query("desc", description="Sort order (asc or desc)")
    ) -> Dict[str, Any]:
        """Get a list of brands.

        Args:
            limit: Maximum number of brands to return
            offset: Offset for pagination
            creator: Filter by creator address
            sort: Sort field
            order: Sort order (asc or desc)

        Returns:
            List of brands and count

        Raises:
            HTTPException: If the index is not initialized or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            brands = await self.index.get_brands(
                limit=limit,
                offset=offset,
                creator=creator,
                sort=sort,
                order=order
            )
            return {"brands": brands, "count": len(brands)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_brand(
        self,
        brand_hash: str = Path(..., description="Brand hash")
    ) -> Dict[str, Any]:
        """Get a brand by its hash.

        Args:
            brand_hash: Brand hash

        Returns:
            Brand information

        Raises:
            HTTPException: If the index is not initialized, brand is not found, or an error occurs
        """
        if not self.index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        try:
            brand = await self.index.get_brand(brand_hash)
            if not brand:
                raise HTTPException(status_code=404, detail="Brand not found")
            
            return brand
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def build_brand(
        self,
        brand_data: Dict[str, Any] = Body(..., description="Brand data")
    ) -> Dict[str, Any]:
        """Build a brand from request data.

        Args:
            brand_data: Brand data

        Returns:
            Built brand

        Raises:
            HTTPException: If an error occurs during building
        """
        try:
            builder = BrandBuilder(config=self.config)
            
            # Set basic properties
            if "name" in brand_data:
                builder.name(brand_data["name"])
            
            if "description" in brand_data:
                builder.description(brand_data["description"])
            
            if "logo" in brand_data:
                builder.logo(brand_data["logo"])
            
            # Set URLs and colors
            if "urls" in brand_data:
                builder.set_urls(brand_data["urls"])
            
            if "colors" in brand_data:
                builder.set_colors(brand_data["colors"])
            
            # Set CTA
            if "cta" in brand_data:
                cta = brand_data["cta"]
                builder.set_cta(
                    title=cta.get("title", ""),
                    description=cta.get("description", ""),
                    label=cta.get("label", ""),
                    url=cta.get("url", "")
                )
            
            # Set metadata properties
            if "metadata" in brand_data:
                metadata = brand_data["metadata"]
                
                if "creator" in metadata:
                    builder.creator(metadata["creator"])
                
                if "createdAt" in metadata:
                    builder.created_at(metadata["createdAt"])
            
            # Build the brand
            built_brand = builder.build()
            
            return built_brand
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class RegistryRoutes:
    """Registry routes for FastAPI."""

    def __init__(
        self,
        config: Config,
        registry: Registry,
        prefix: str = "/registry"
    ):
        """Initialize Registry routes.

        Args:
            config: SDK configuration
            registry: Registry instance
            prefix: Route prefix
        """
        self.config = config
        self.registry = registry
        self.router = APIRouter(prefix=prefix)
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up routes."""
        self.router.add_api_route(
            "/{tx_hash}",
            self.get_registry_info,
            methods=["GET"],
            summary="Get Registry Info",
            description="Get registry information for a Warp."
        )

    async def get_registry_info(
        self,
        tx_hash: str = Path(..., description="Transaction hash of the Warp")
    ) -> Dict[str, Any]:
        """Get registry information for a Warp.

        Args:
            tx_hash: Transaction hash

        Returns:
            Registry information

        Raises:
            HTTPException: If the registry is not initialized, info is not found, or an error occurs
        """
        try:
            info = await self.registry.get_registry_info(tx_hash)
            if not info:
                raise HTTPException(status_code=404, detail="Registry information not found")
            
            return info
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def create_warp_routes(
    config: Config,
    registry: Optional[Registry] = None,
    index: Optional[Index] = None,
    prefix: str = "/warps"
) -> WarpRoutes:
    """Create Warp routes.

    Args:
        config: SDK configuration
        registry: Registry instance
        index: Index instance
        prefix: Route prefix

    Returns:
        WarpRoutes instance
    """
    return WarpRoutes(
        config=config,
        registry=registry,
        index=index,
        prefix=prefix
    )


def create_brand_routes(
    config: Config,
    registry: Optional[Registry] = None,
    index: Optional[Index] = None,
    prefix: str = "/brands"
) -> BrandRoutes:
    """Create Brand routes.

    Args:
        config: SDK configuration
        registry: Registry instance
        index: Index instance
        prefix: Route prefix

    Returns:
        BrandRoutes instance
    """
    return BrandRoutes(
        config=config,
        registry=registry,
        index=index,
        prefix=prefix
    )


def create_registry_routes(
    config: Config,
    registry: Registry,
    prefix: str = "/registry"
) -> RegistryRoutes:
    """Create Registry routes.

    Args:
        config: SDK configuration
        registry: Registry instance
        prefix: Route prefix

    Returns:
        RegistryRoutes instance
    """
    return RegistryRoutes(
        config=config,
        registry=registry,
        prefix=prefix
    )
