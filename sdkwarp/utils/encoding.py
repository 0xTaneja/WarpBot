"""Encoding utilities for the SDK."""

import base64
from typing import Union


def encode_base64(data: Union[str, bytes]) -> str:
    """Encode data to base64.

    Args:
        data: Data to encode (string or bytes)

    Returns:
        Base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data: str) -> str:
    """Decode base64 data to string.

    Args:
        data: Base64 encoded string

    Returns:
        Decoded string

    Raises:
        ValueError: If the data is not valid base64
    """
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decode base64 data: {e}")


def encode_hex(data: Union[str, bytes]) -> str:
    """Encode data to hexadecimal.

    Args:
        data: Data to encode (string or bytes)

    Returns:
        Hexadecimal encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return data.hex()


def decode_hex(data: str) -> bytes:
    """Decode hexadecimal data to bytes.

    Args:
        data: Hexadecimal encoded string

    Returns:
        Decoded bytes

    Raises:
        ValueError: If the data is not valid hexadecimal
    """
    try:
        return bytes.fromhex(data)
    except Exception as e:
        raise ValueError(f"Failed to decode hex data: {e}") 