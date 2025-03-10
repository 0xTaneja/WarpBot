"""Cache module for caching contract data."""

import json
import os
import time
from typing import Dict, Any, Optional, List, Union, Callable

from sdkwarp.config.models import Config


class Cache:
    """Cache for contract data."""

    def __init__(self, config: Config):
        """Initialize the cache.

        Args:
            config: SDK configuration
        """
        self.config = config
        self._initialized = False
        self._memory_cache = {}
        self._cache_dir = None
        self._default_ttl = 3600  # 1 hour in seconds

    async def init(self) -> None:
        """Initialize the cache.

        Sets up the cache directory if configured.
        """
        # Set up cache directory if configured
        if self.config.cache_directory:
            self._cache_dir = self.config.cache_directory
            os.makedirs(self._cache_dir, exist_ok=True)
        
        # Set default TTL if configured
        if self.config.cache_ttl:
            self._default_ttl = self.config.cache_ttl
        
        self._initialized = True

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        # Check memory cache first
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if entry["expires"] > time.time():
                return entry["value"]
            else:
                # Remove expired entry
                del self._memory_cache[key]
        
        # If not in memory cache, check file cache if enabled
        if self._cache_dir:
            file_path = os.path.join(self._cache_dir, f"{key}.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as f:
                        entry = json.load(f)
                    
                    if entry["expires"] > time.time():
                        # Add to memory cache
                        self._memory_cache[key] = entry
                        return entry["value"]
                    else:
                        # Remove expired file
                        os.remove(file_path)
                except Exception:
                    # Ignore errors and return None
                    pass
        
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (defaults to configured TTL)
        """
        # Use default TTL if not specified
        ttl = ttl if ttl is not None else self._default_ttl
        
        # Create cache entry
        expires = time.time() + ttl
        entry = {
            "value": value,
            "expires": expires
        }
        
        # Store in memory cache
        self._memory_cache[key] = entry
        
        # Store in file cache if enabled
        if self._cache_dir:
            file_path = os.path.join(self._cache_dir, f"{key}.json")
            try:
                with open(file_path, "w") as f:
                    json.dump(entry, f)
            except Exception:
                # Ignore errors
                pass

    def delete(self, key: str) -> None:
        """Delete a value from the cache.

        Args:
            key: Cache key
        """
        # Remove from memory cache
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        # Remove from file cache if enabled
        if self._cache_dir:
            file_path = os.path.join(self._cache_dir, f"{key}.json")
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    # Ignore errors
                    pass

    def clear(self) -> None:
        """Clear the entire cache."""
        # Clear memory cache
        self._memory_cache = {}
        
        # Clear file cache if enabled
        if self._cache_dir:
            try:
                for filename in os.listdir(self._cache_dir):
                    if filename.endswith(".json"):
                        os.remove(os.path.join(self._cache_dir, filename))
            except Exception:
                # Ignore errors
                pass

    def get_or_set(
        self,
        key: str,
        callback: Callable[[], Any],
        ttl: Optional[int] = None
    ) -> Any:
        """Get a value from the cache or set it if not found.

        Args:
            key: Cache key
            callback: Function to call to get the value if not in cache
            ttl: Time to live in seconds (defaults to configured TTL)

        Returns:
            Cached value or result of callback
        """
        # Try to get from cache first
        value = self.get(key)
        if value is not None:
            return value
        
        # If not in cache, call the callback
        value = callback()
        
        # Store in cache
        self.set(key, value, ttl)
        
        return value

    async def get_or_set_async(
        self,
        key: str,
        callback: Callable[[], Any],
        ttl: Optional[int] = None
    ) -> Any:
        """Get a value from the cache or set it if not found (async version).

        Args:
            key: Cache key
            callback: Async function to call to get the value if not in cache
            ttl: Time to live in seconds (defaults to configured TTL)

        Returns:
            Cached value or result of callback
        """
        # Try to get from cache first
        value = self.get(key)
        if value is not None:
            return value
        
        # If not in cache, call the callback
        value = await callback()
        
        # Store in cache
        self.set(key, value, ttl)
        
        return value
