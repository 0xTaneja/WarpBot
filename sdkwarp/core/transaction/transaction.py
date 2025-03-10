"""Transaction module for handling blockchain transactions."""

import json
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import TransactionData


class Transaction:
    """Transaction class for handling blockchain transactions."""

    def __init__(
        self,
        sender: str,
        receiver: str,
        value: str,
        data: str = "",
        gas_limit: int = 50000,
        chain_id: str = "D",
        version: int = 1,
        options: Optional[Dict[str, Any]] = None,
        nonce: Optional[int] = None
    ):
        """Initialize a transaction.

        Args:
            sender: Sender address
            receiver: Receiver address
            value: Transaction value (in atomic units)
            data: Transaction data
            gas_limit: Gas limit
            chain_id: Chain ID
            version: Transaction version
            options: Additional options
            nonce: Transaction nonce
        """
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.data = data
        self.gas_limit = gas_limit
        self.chain_id = chain_id
        self.version = version
        self.options = options or {}
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary.

        Returns:
            Transaction as dictionary
        """
        result = {
            "sender": self.sender,
            "receiver": self.receiver,
            "value": self.value,
            "data": self.data,
            "gasLimit": self.gas_limit,
            "chainID": self.chain_id,
            "version": self.version
        }
        
        if self.nonce is not None:
            result["nonce"] = self.nonce
        
        if self.options:
            result["options"] = self.options
        
        return result

    def to_json(self) -> str:
        """Convert transaction to JSON.

        Returns:
            Transaction as JSON string
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary.

        Args:
            data: Transaction data as dictionary

        Returns:
            Transaction instance
        """
        return cls(
            sender=data.get("sender", ""),
            receiver=data.get("receiver", ""),
            value=data.get("value", "0"),
            data=data.get("data", ""),
            gas_limit=data.get("gasLimit", 50000),
            chain_id=data.get("chainID", "D"),
            version=data.get("version", 1),
            options=data.get("options"),
            nonce=data.get("nonce")
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'Transaction':
        """Create transaction from JSON.

        Args:
            json_str: Transaction data as JSON string

        Returns:
            Transaction instance

        Raises:
            ValueError: If the JSON is invalid
        """
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except Exception as e:
            raise ValueError(f"Failed to parse transaction JSON: {e}")

    @classmethod
    def from_model(cls, model: TransactionData) -> 'Transaction':
        """Create transaction from TransactionData model.

        Args:
            model: TransactionData instance

        Returns:
            Transaction instance
        """
        return cls(
            sender=model.sender,
            receiver=model.receiver,
            value=model.value,
            data=model.data,
            gas_limit=model.gas_limit,
            chain_id=model.chain_id,
            version=model.version,
            options=model.options,
            nonce=model.nonce
        )

    def to_model(self) -> TransactionData:
        """Convert transaction to TransactionData model.

        Returns:
            TransactionData instance
        """
        return TransactionData(
            sender=self.sender,
            receiver=self.receiver,
            value=self.value,
            data=self.data,
            gas_limit=self.gas_limit,
            chain_id=self.chain_id,
            version=self.version,
            options=self.options,
            nonce=self.nonce
        ) 