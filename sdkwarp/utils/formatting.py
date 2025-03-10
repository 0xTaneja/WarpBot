"""Formatting utilities for the SDK."""

import re
from typing import Optional


def format_address(address: str, short: bool = False) -> str:
    """Format MultiversX address.
    
    Args:
        address: Address to format
        short: Whether to return a shortened version
    
    Returns:
        Formatted address
    """
    if not address:
        return ""
    
    # Ensure address starts with erd1
    if not address.startswith("erd1"):
        return address
    
    if short:
        # Return first 8 and last 4 characters
        return f"{address[:8]}...{address[-4:]}"
    
    return address


def format_amount(amount: str, decimals: int = 18, symbol: Optional[str] = None) -> str:
    """Format token amount.
    
    Args:
        amount: Amount to format (as string)
        decimals: Token decimals
        symbol: Token symbol
    
    Returns:
        Formatted amount
    """
    if not amount:
        return "0"
    
    try:
        # Convert to float
        value = int(amount) / (10 ** decimals)
        
        # Format with appropriate precision
        if value == 0:
            formatted = "0"
        elif value < 0.001:
            formatted = f"{value:.8f}".rstrip("0").rstrip(".")
        elif value < 1:
            formatted = f"{value:.6f}".rstrip("0").rstrip(".")
        elif value < 1000:
            formatted = f"{value:.4f}".rstrip("0").rstrip(".")
        else:
            formatted = f"{value:,.2f}".rstrip("0").rstrip(".")
        
        # Add symbol if provided
        if symbol:
            return f"{formatted} {symbol}"
        
        return formatted
    
    except (ValueError, TypeError):
        return amount


def format_data(data: str, max_length: int = 50) -> str:
    """Format transaction data.
    
    Args:
        data: Transaction data to format
        max_length: Maximum length before truncation
    
    Returns:
        Formatted data
    """
    if not data:
        return ""
    
    # Remove whitespace
    data = re.sub(r"\s+", "", data)
    
    # Truncate if too long
    if len(data) > max_length:
        return f"{data[:max_length]}..."
    
    return data
