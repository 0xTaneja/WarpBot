"""Encoding and decoding utilities for the SDK."""

import json
import base64
from typing import Any, Dict, List, Optional, Union


class Codec:
    """Encoding and decoding utilities."""
    
    @staticmethod
    def encode_json(data: Any) -> str:
        """Encode data as JSON string.
        
        Args:
            data: Data to encode
        
        Returns:
            JSON string
        """
        return json.dumps(data, separators=(",", ":"))
    
    @staticmethod
    def decode_json(data: str) -> Any:
        """Decode JSON string.
        
        Args:
            data: JSON string to decode
        
        Returns:
            Decoded data
        """
        return json.loads(data)
    
    @staticmethod
    def encode_base64(data: Union[str, bytes]) -> str:
        """Encode data as base64 string.
        
        Args:
            data: Data to encode
        
        Returns:
            Base64 string
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        
        return base64.b64encode(data).decode("utf-8")
    
    @staticmethod
    def decode_base64(data: str) -> bytes:
        """Decode base64 string.
        
        Args:
            data: Base64 string to decode
        
        Returns:
            Decoded data
        """
        return base64.b64decode(data)
    
    @staticmethod
    def decode_base64_to_str(data: str) -> str:
        """Decode base64 string to UTF-8 string.
        
        Args:
            data: Base64 string to decode
        
        Returns:
            Decoded string
        """
        return Codec.decode_base64(data).decode("utf-8")
    
    @staticmethod
    def encode_hex(data: Union[str, bytes]) -> str:
        """Encode data as hex string.
        
        Args:
            data: Data to encode
        
        Returns:
            Hex string
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        
        return data.hex()
    
    @staticmethod
    def decode_hex(data: str) -> bytes:
        """Decode hex string.
        
        Args:
            data: Hex string to decode
        
        Returns:
            Decoded data
        """
        return bytes.fromhex(data)
    
    @staticmethod
    def decode_hex_to_str(data: str) -> str:
        """Decode hex string to UTF-8 string.
        
        Args:
            data: Hex string to decode
        
        Returns:
            Decoded string
        """
        return Codec.decode_hex(data).decode("utf-8")
    
    @staticmethod
    def encode_transaction_data(data: Dict[str, Any]) -> str:
        """Encode transaction data.
        
        Args:
            data: Transaction data
        
        Returns:
            Encoded transaction data
        """
        json_data = Codec.encode_json(data)
        return Codec.encode_base64(json_data)
    
    @staticmethod
    def decode_transaction_data(data: str) -> Dict[str, Any]:
        """Decode transaction data.
        
        Args:
            data: Encoded transaction data
        
        Returns:
            Decoded transaction data
        """
        json_data = Codec.decode_base64_to_str(data)
        return Codec.decode_json(json_data)
