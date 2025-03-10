"""FastAPI integration for the SDK."""

import json
from typing import Dict, Any, Optional, List, Union, Callable

try:
    from fastapi import FastAPI, APIRouter, Query, Path, Body, HTTPException, Depends
    from pydantic import BaseModel, Field
except ImportError:
    raise ImportError("FastAPI is not installed. Install it with 'pip install fastapi'.")

from sdkwarp.config.models import Config
from sdkwarp.core.registry import Registry, Index
from sdkwarp.core.builder import WarpBuilder, BrandBuilder


# Pydantic models for request/response
class WarpAction(BaseModel):
    """Warp action model."""
    
    type: str = Field(..., description="Action type")
    title: str = Field(..., description="Action title")
    description: str = Field(..., description="Action description")
    data: Dict[str, Any] = Field(default_factory=dict, description="Action data")


class WarpMetadata(BaseModel):
    """Warp metadata model."""
    
    creator: Optional[str] = Field(None, description="Creator address")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")


class Warp(BaseModel):
    """Warp model."""
    
    name: str = Field(..., description="Warp name")
    title: str = Field(..., description="Warp title")
    description: str = Field(..., description="Warp description")
    action: WarpAction = Field(..., description="Warp action")
    metadata: WarpMetadata = Field(default_factory=WarpMetadata, description="Warp metadata")


class BrandCTA(BaseModel):
    """Brand CTA model."""
    
    title: str = Field(..., description="CTA title")
    description: str = Field(..., description="CTA description")
    label: str = Field(..., description="CTA button label")
    url: str = Field(..., description="CTA URL")


class BrandMetadata(BaseModel):
    """Brand metadata model."""
    
    creator: Optional[str] = Field(None, description="Creator address")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")


class Brand(BaseModel):
    """Brand model."""
    
    name: str = Field(..., description="Brand name")
    description: str = Field(..., description="Brand description")
    logo: str = Field(..., description="Brand logo URL")
    urls: Dict[str, str] = Field(default_factory=dict, description="Brand URLs")
    colors: Dict[str, str] = Field(default_factory=dict, description="Brand colors")
    cta: BrandCTA = Field(..., description="Brand CTA")
    metadata: BrandMetadata = Field(default_factory=BrandMetadata, description="Brand metadata")


class WarpsResponse(BaseModel):
    """Warps response model."""
    
    warps: List[Dict[str, Any]] = Field(..., description="List of Warps")
    count: int = Field(..., description="Number of Warps")


class BrandsResponse(BaseModel):
    """Brands response model."""
    
    brands: List[Dict[str, Any]] = Field(..., description="List of brands")
    count: int = Field(..., description="Number of brands")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")


class FastAPI:
    """FastAPI integration for the SDK."""

    def __init__(
        self,
        config: Config,
        registry: Optional[Registry] = None,
        index: Optional[Index] = None,
        router_prefix: str = "/api/warp"
    ):
        """Initialize the FastAPI integration.

        Args:
            config: SDK configuration
            registry: Registry instance
            index: Index instance
            router_prefix: Router prefix for the API
        """
        self.config = config
        self.registry = registry
        self.index = index
        self.router_prefix = router_prefix
        self.router = APIRouter(prefix=router_prefix)
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up API routes."""
        # Warp routes
        self.router.add_api_route(
            "/warps",
            self.get_warps,
            methods=["GET"],
            response_model=WarpsResponse,
            summary="Get Warps",
            description="Get a list of Warps with pagination and filtering options."
        )
        
        self.router.add_api_route(
            "/warps/{tx_hash}",
            self.get_warp,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Get Warp",
            description="Get a Warp by its transaction hash."
        )
        
        self.router.add_api_route(
            "/warps/alias/{alias}",
            self.get_warp_by_alias,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Get Warp by Alias",
            description="Get a Warp by its alias."
        )
        
        self.router.add_api_route(
            "/warps/search",
            self.search_warps,
            methods=["GET"],
            response_model=WarpsResponse,
            summary="Search Warps",
            description="Search for Warps by name, title, or description."
        )
        
        # Brand routes
        self.router.add_api_route(
            "/brands",
            self.get_brands,
            methods=["GET"],
            response_model=BrandsResponse,
            summary="Get Brands",
            description="Get a list of brands with pagination and filtering options."
        )
        
        self.router.add_api_route(
            "/brands/{brand_hash}",
            self.get_brand,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Get Brand",
            description="Get a brand by its hash."
        )
        
        # Registry routes
        self.router.add_api_route(
            "/registry/{tx_hash}",
            self.get_registry_info,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Get Registry Info",
            description="Get registry information for a Warp."
        )
        
        # Builder routes
        self.router.add_api_route(
            "/builder/warp",
            self.build_warp,
            methods=["POST"],
            response_model=Dict[str, Any],
            summary="Build Warp",
            description="Build a Warp from request data."
        )
        
        self.router.add_api_route(
            "/builder/brand",
            self.build_brand,
            methods=["POST"],
            response_model=Dict[str, Any],
            summary="Build Brand",
            description="Build a brand from request data."
        )

    def register(self, app: FastAPI) -> None:
        """Register the router with a FastAPI app.

        Args:
            app: FastAPI application
        """
        app.include_router(self.router)

    async def get_warps(
        self,
        limit: int = Query(10, ge=1, le=100, description="Maximum number of Warps to return"),
        offset: int = Query(0, ge=0, description="Offset for pagination"),
        creator: Optional[str] = Query(None, description="Filter by creator address"),
        sort: str = Query("createdAt", description="Sort field"),
        order: str = Query("desc", description="Sort order (asc or desc)")
    ) -> WarpsResponse:
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
    ) -> WarpsResponse:
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

    async def get_brands(
        self,
        limit: int = Query(10, ge=1, le=100, description="Maximum number of brands to return"),
        offset: int = Query(0, ge=0, description="Offset for pagination"),
        creator: Optional[str] = Query(None, description="Filter by creator address"),
        sort: str = Query("createdAt", description="Sort field"),
        order: str = Query("desc", description="Sort order (asc or desc)")
    ) -> BrandsResponse:
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
        if not self.registry:
            raise HTTPException(status_code=500, detail="Registry not initialized")
        
        try:
            info = await self.registry.get_registry_info(tx_hash)
            if not info:
                raise HTTPException(status_code=404, detail="Registry information not found")
            
            return info
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def build_warp(
        self,
        warp: Warp = Body(..., description="Warp data")
    ) -> Dict[str, Any]:
        """Build a Warp from request data.

        Args:
            warp: Warp data

        Returns:
            Built Warp

        Raises:
            HTTPException: If an error occurs during building
        """
        try:
            builder = WarpBuilder(config=self.config)
            
            # Set basic properties
            builder.name(warp.name)
            builder.title(warp.title)
            builder.description(warp.description)
            
            # Set action properties
            builder.action_type(warp.action.type)
            builder.action_title(warp.action.title)
            builder.action_description(warp.action.description)
            builder.action_data(warp.action.data)
            
            # Set metadata properties
            if warp.metadata.creator:
                builder.creator(warp.metadata.creator)
            
            if warp.metadata.createdAt:
                builder.created_at(warp.metadata.createdAt)
            
            # Build the Warp
            built_warp = builder.build()
            
            return built_warp
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def build_brand(
        self,
        brand: Brand = Body(..., description="Brand data")
    ) -> Dict[str, Any]:
        """Build a brand from request data.

        Args:
            brand: Brand data

        Returns:
            Built brand

        Raises:
            HTTPException: If an error occurs during building
        """
        try:
            builder = BrandBuilder(config=self.config)
            
            # Set basic properties
            builder.name(brand.name)
            builder.description(brand.description)
            builder.logo(brand.logo)
            
            # Set URLs and colors
            builder.set_urls(brand.urls)
            builder.set_colors(brand.colors)
            
            # Set CTA
            builder.set_cta(
                title=brand.cta.title,
                description=brand.cta.description,
                label=brand.cta.label,
                url=brand.cta.url
            )
            
            # Set metadata properties
            if brand.metadata.creator:
                builder.creator(brand.metadata.creator)
            
            if brand.metadata.createdAt:
                builder.created_at(brand.metadata.createdAt)
            
            # Build the brand
            built_brand = builder.build()
            
            return built_brand
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def create_fastapi_api(
    config: Config,
    registry: Optional[Registry] = None,
    index: Optional[Index] = None,
    router_prefix: str = "/api/warp"
) -> FastAPI:
    """Create a FastAPI integration instance.

    Args:
        config: SDK configuration
        registry: Registry instance
        index: Index instance
        router_prefix: Router prefix for the API

    Returns:
        FastAPI integration instance
    """
    return FastAPI(
        config=config,
        registry=registry,
        index=index,
        router_prefix=router_prefix
    )
