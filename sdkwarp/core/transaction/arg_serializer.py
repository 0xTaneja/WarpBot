"""Argument serializer module for transaction arguments."""

import json
from typing import Dict, Any, List, Union, Optional

from sdkwarp.utils.encoding import encode_base64, encode_hex


class ArgSerializer:
    """Argument serializer for transaction arguments."""

    @staticmethod
    def serialize_args(args: List[Any]) -> str:
        """Serialize a list of arguments for a transaction.

        Args:
            args: List of arguments

        Returns:
            Serialized arguments string
        """
        if not args:
            return ""
        
        serialized_args = []
        for arg in args:
            serialized_args.append(ArgSerializer.serialize_arg(arg))
        
        return "@".join(serialized_args)

    @staticmethod
    def serialize_arg(arg: Any) -> str:
        """Serialize a single argument for a transaction.

        Args:
            arg: Argument to serialize

        Returns:
            Serialized argument string

        Raises:
            ValueError: If the argument type is not supported
        """
        if arg is None:
            return ""
        
        if isinstance(arg, str):
            return encode_base64(arg)
        
        if isinstance(arg, int):
            return encode_base64(str(arg))
        
        if isinstance(arg, bool):
            return encode_base64("true" if arg else "false")
        
        if isinstance(arg, (list, tuple)):
            return encode_base64(json.dumps(arg))
        
        if isinstance(arg, dict):
            return encode_base64(json.dumps(arg))
        
        if isinstance(arg, bytes):
            return encode_hex(arg)
        
        raise ValueError(f"Unsupported argument type: {type(arg)}")

    @staticmethod
    def serialize_function_call(
        function: str,
        args: Optional[List[Any]] = None
    ) -> str:
        """Serialize a function call for a transaction.

        Args:
            function: Function name
            args: Function arguments

        Returns:
            Serialized function call string
        """
        if not args:
            return function
        
        serialized_args = ArgSerializer.serialize_args(args)
        if not serialized_args:
            return function
        
        return f"{function}@{serialized_args}"

    @staticmethod
    def serialize_esdt_transfer(
        token_id: str,
        amount: Union[str, int],
        function: Optional[str] = None,
        args: Optional[List[Any]] = None
    ) -> str:
        """Serialize an ESDT transfer for a transaction.

        Args:
            token_id: Token identifier
            amount: Amount to transfer
            function: Optional function to call
            args: Optional function arguments

        Returns:
            Serialized ESDT transfer string
        """
        # Convert amount to string if it's an integer
        if isinstance(amount, int):
            amount = str(amount)
        
        # Base ESDT transfer
        result = f"ESDTTransfer@{encode_base64(token_id)}@{encode_base64(amount)}"
        
        # Add function call if provided
        if function:
            result += f"@{encode_base64(function)}"
            
            # Add arguments if provided
            if args:
                for arg in args:
                    result += f"@{ArgSerializer.serialize_arg(arg)}"
        
        return result

    @staticmethod
    def serialize_esdt_nft_transfer(
        token_id: str,
        nonce: Union[str, int],
        amount: Union[str, int],
        receiver: str,
        function: Optional[str] = None,
        args: Optional[List[Any]] = None
    ) -> str:
        """Serialize an ESDT NFT transfer for a transaction.

        Args:
            token_id: Token identifier
            nonce: NFT nonce
            amount: Amount to transfer
            receiver: Receiver address
            function: Optional function to call
            args: Optional function arguments

        Returns:
            Serialized ESDT NFT transfer string
        """
        # Convert nonce and amount to string if they're integers
        if isinstance(nonce, int):
            nonce = str(nonce)
        
        if isinstance(amount, int):
            amount = str(amount)
        
        # Base ESDT NFT transfer
        result = (
            f"ESDTNFTTransfer@{encode_base64(token_id)}@{encode_base64(nonce)}"
            f"@{encode_base64(amount)}@{encode_base64(receiver)}"
        )
        
        # Add function call if provided
        if function:
            result += f"@{encode_base64(function)}"
            
            # Add arguments if provided
            if args:
                for arg in args:
                    result += f"@{ArgSerializer.serialize_arg(arg)}"
        
        return result

    @staticmethod
    def serialize_multi_esdt_transfer(
        transfers: List[Dict[str, Any]],
        function: Optional[str] = None,
        args: Optional[List[Any]] = None
    ) -> str:
        """Serialize a multi ESDT transfer for a transaction.

        Args:
            transfers: List of transfers, each with token_id, nonce (optional), and amount
            function: Optional function to call
            args: Optional function arguments

        Returns:
            Serialized multi ESDT transfer string

        Raises:
            ValueError: If the transfers list is empty or invalid
        """
        if not transfers:
            raise ValueError("Transfers list cannot be empty")
        
        # Number of transfers
        result = f"MultiESDTNFTTransfer@{encode_base64(str(len(transfers)))}"
        
        # Add each transfer
        for transfer in transfers:
            token_id = transfer.get("token_id")
            if not token_id:
                raise ValueError("Missing token_id in transfer")
            
            amount = transfer.get("amount")
            if not amount:
                raise ValueError("Missing amount in transfer")
            
            # Convert amount to string if it's an integer
            if isinstance(amount, int):
                amount = str(amount)
            
            # Add token ID
            result += f"@{encode_base64(token_id)}"
            
            # Add nonce if present (0 for fungible tokens)
            nonce = transfer.get("nonce", "0")
            if isinstance(nonce, int):
                nonce = str(nonce)
            
            result += f"@{encode_base64(nonce)}"
            
            # Add amount
            result += f"@{encode_base64(amount)}"
        
        # Add function call if provided
        if function:
            result += f"@{encode_base64(function)}"
            
            # Add arguments if provided
            if args:
                for arg in args:
                    result += f"@{ArgSerializer.serialize_arg(arg)}"
        
        return result 