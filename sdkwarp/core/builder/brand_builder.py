"""Brand builder module for building brand objects."""

import json
import time
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config
from sdkwarp.utils.validation import Validator


class BrandBuilder:
    """Builder for creating brand objects."""

    def __init__(
        self,
        config: Optional[Config] = None,
        validator: Optional[Validator] = None
    ):
        """Initialize the brand builder.

        Args:
            config: SDK configuration
            validator: Validator instance
        """
        self.config = config
        self.validator = validator or Validator()
        self._brand = {
            "name": "",
            "description": "",
            "logo": "",
            "urls": {},
            "colors": {},
            "cta": {
                "title": "",
                "description": "",
                "label": "",
                "url": ""
            },
            "metadata": {
                "creator": "",
                "createdAt": ""
            }
        }

    def name(self, name: str) -> 'BrandBuilder':
        """Set the brand name.

        Args:
            name: Brand name

        Returns:
            Self for chaining
        """
        self._brand["name"] = name
        return self

    def description(self, description: str) -> 'BrandBuilder':
        """Set the brand description.

        Args:
            description: Brand description

        Returns:
            Self for chaining
        """
        self._brand["description"] = description
        return self

    def logo(self, logo: str) -> 'BrandBuilder':
        """Set the brand logo URL.

        Args:
            logo: Logo URL

        Returns:
            Self for chaining
        """
        self._brand["logo"] = logo
        return self

    def add_url(self, key: str, url: str) -> 'BrandBuilder':
        """Add a URL to the brand.

        Args:
            key: URL key (e.g., "web", "twitter", "discord")
            url: URL value

        Returns:
            Self for chaining
        """
        self._brand["urls"][key] = url
        return self

    def set_urls(self, urls: Dict[str, str]) -> 'BrandBuilder':
        """Set all URLs for the brand.

        Args:
            urls: Dictionary of URLs

        Returns:
            Self for chaining
        """
        self._brand["urls"] = urls
        return self

    def add_color(self, key: str, color: str) -> 'BrandBuilder':
        """Add a color to the brand.

        Args:
            key: Color key (e.g., "primary", "secondary")
            color: Color value (hex code)

        Returns:
            Self for chaining
        """
        self._brand["colors"][key] = color
        return self

    def set_colors(self, colors: Dict[str, str]) -> 'BrandBuilder':
        """Set all colors for the brand.

        Args:
            colors: Dictionary of colors

        Returns:
            Self for chaining
        """
        self._brand["colors"] = colors
        return self

    def cta_title(self, title: str) -> 'BrandBuilder':
        """Set the CTA title.

        Args:
            title: CTA title

        Returns:
            Self for chaining
        """
        self._brand["cta"]["title"] = title
        return self

    def cta_description(self, description: str) -> 'BrandBuilder':
        """Set the CTA description.

        Args:
            description: CTA description

        Returns:
            Self for chaining
        """
        self._brand["cta"]["description"] = description
        return self

    def cta_label(self, label: str) -> 'BrandBuilder':
        """Set the CTA button label.

        Args:
            label: CTA button label

        Returns:
            Self for chaining
        """
        self._brand["cta"]["label"] = label
        return self

    def cta_url(self, url: str) -> 'BrandBuilder':
        """Set the CTA URL.

        Args:
            url: CTA URL

        Returns:
            Self for chaining
        """
        self._brand["cta"]["url"] = url
        return self

    def set_cta(
        self,
        title: str,
        description: str,
        label: str,
        url: str
    ) -> 'BrandBuilder':
        """Set the complete CTA.

        Args:
            title: CTA title
            description: CTA description
            label: CTA button label
            url: CTA URL

        Returns:
            Self for chaining
        """
        self._brand["cta"] = {
            "title": title,
            "description": description,
            "label": label,
            "url": url
        }
        return self

    def creator(self, creator: str) -> 'BrandBuilder':
        """Set the creator address.

        Args:
            creator: Creator address

        Returns:
            Self for chaining
        """
        self._brand["metadata"]["creator"] = creator
        return self

    def created_at(self, timestamp: Union[str, int]) -> 'BrandBuilder':
        """Set the creation timestamp.

        Args:
            timestamp: Creation timestamp (ISO string or Unix timestamp)

        Returns:
            Self for chaining
        """
        if isinstance(timestamp, int):
            # Convert Unix timestamp to ISO string
            from datetime import datetime
            dt = datetime.fromtimestamp(timestamp)
            timestamp = dt.isoformat()
        
        self._brand["metadata"]["createdAt"] = timestamp
        return self

    def build(self) -> Dict[str, Any]:
        """Build the brand object.

        Returns:
            Brand object

        Raises:
            ValueError: If the brand is invalid
        """
        # Set default values if not set
        if not self._brand["metadata"]["creator"] and self.config and self.config.user_address:
            self._brand["metadata"]["creator"] = self.config.user_address
        
        if not self._brand["metadata"]["createdAt"]:
            self._brand["metadata"]["createdAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        # Clean up empty objects
        if not self._brand["urls"]:
            self._brand["urls"] = {"web": ""}
        
        if not self._brand["colors"]:
            self._brand["colors"] = {"primary": "#000000", "secondary": "#FFFFFF"}
        
        # Validate the brand
        if not self.validator.validate_brand(self._brand):
            raise ValueError("Invalid brand schema")
        
        return self._brand

    def to_json(self) -> str:
        """Convert the brand to JSON.

        Returns:
            Brand as JSON string
        """
        return json.dumps(self.build(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'BrandBuilder':
        """Create a BrandBuilder from JSON.

        Args:
            json_str: JSON string

        Returns:
            BrandBuilder instance

        Raises:
            ValueError: If the JSON is invalid
        """
        try:
            brand = json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")
        
        return cls.from_dict(brand)

    @classmethod
    def from_dict(cls, brand: Dict[str, Any]) -> 'BrandBuilder':
        """Create a BrandBuilder from a dictionary.

        Args:
            brand: Brand dictionary

        Returns:
            BrandBuilder instance
        """
        builder = cls()
        
        # Set basic properties
        if "name" in brand:
            builder.name(brand["name"])
        
        if "description" in brand:
            builder.description(brand["description"])
        
        if "logo" in brand:
            builder.logo(brand["logo"])
        
        # Set URLs
        if "urls" in brand and isinstance(brand["urls"], dict):
            builder.set_urls(brand["urls"])
        
        # Set colors
        if "colors" in brand and isinstance(brand["colors"], dict):
            builder.set_colors(brand["colors"])
        
        # Set CTA
        cta = brand.get("cta", {})
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
        metadata = brand.get("metadata", {})
        
        if "creator" in metadata:
            builder.creator(metadata["creator"])
        
        if "createdAt" in metadata:
            builder.created_at(metadata["createdAt"])
        
        return builder

    def create_inscription_transaction(self, brand: Dict[str, Any]) -> "Transaction":
        """Create an inscription transaction for the Brand.

        Args:
            brand: Brand object

        Returns:
            Transaction object
        """
        from sdkwarp.core.transaction import Transaction
        
        # Create a dummy transaction for now
        # In a real implementation, this would create a proper transaction
        return Transaction(
            sender="erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
            receiver="erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
            value="0",
            data="BRAND-INSCRIPTION",
            gas_limit=50000,
            chain_id="D"
        )
