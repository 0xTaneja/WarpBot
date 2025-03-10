"""Warp builder module for building Warp objects."""

import json
import time
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config
from sdkwarp.utils.validation import Validator


class WarpBuilder:
    """Builder for creating Warp objects."""

    def __init__(
        self,
        config: Optional[Config] = None,
        validator: Optional[Validator] = None
    ):
        """Initialize the Warp builder.

        Args:
            config: SDK configuration
            validator: Validator instance
        """
        self.config = config
        self.validator = validator or Validator()
        self._warp = {
            "name": "",
            "title": "",
            "description": "",
            "action": {
                "type": "",
                "title": "",
                "description": "",
                "data": {}
            },
            "metadata": {
                "creator": "",
                "createdAt": ""
            }
        }

    def name(self, name: str) -> 'WarpBuilder':
        """Set the Warp name.

        Args:
            name: Warp name

        Returns:
            Self for chaining
        """
        self._warp["name"] = name
        return self

    def title(self, title: str) -> 'WarpBuilder':
        """Set the Warp title.

        Args:
            title: Warp title

        Returns:
            Self for chaining
        """
        self._warp["title"] = title
        return self

    def description(self, description: str) -> 'WarpBuilder':
        """Set the Warp description.

        Args:
            description: Warp description

        Returns:
            Self for chaining
        """
        self._warp["description"] = description
        return self

    def action_type(self, action_type: str) -> 'WarpBuilder':
        """Set the action type.

        Args:
            action_type: Action type

        Returns:
            Self for chaining
        """
        self._warp["action"]["type"] = action_type
        return self

    def action_title(self, title: str) -> 'WarpBuilder':
        """Set the action title.

        Args:
            title: Action title

        Returns:
            Self for chaining
        """
        self._warp["action"]["title"] = title
        return self

    def action_description(self, description: str) -> 'WarpBuilder':
        """Set the action description.

        Args:
            description: Action description

        Returns:
            Self for chaining
        """
        self._warp["action"]["description"] = description
        return self

    def action_data(self, data: Dict[str, Any]) -> 'WarpBuilder':
        """Set the action data.

        Args:
            data: Action data

        Returns:
            Self for chaining
        """
        self._warp["action"]["data"] = data
        return self

    def creator(self, creator: str) -> 'WarpBuilder':
        """Set the creator address.

        Args:
            creator: Creator address

        Returns:
            Self for chaining
        """
        self._warp["metadata"]["creator"] = creator
        return self

    def created_at(self, timestamp: Union[str, int]) -> 'WarpBuilder':
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
        
        self._warp["metadata"]["createdAt"] = timestamp
        return self

    def transfer_action(
        self,
        token: str,
        amount: str,
        recipient: Optional[str] = None
    ) -> 'WarpBuilder':
        """Set a transfer action.

        Args:
            token: Token identifier
            amount: Amount to transfer
            recipient: Recipient address (optional)

        Returns:
            Self for chaining
        """
        self._warp["action"]["type"] = "transfer"
        self._warp["action"]["title"] = f"Transfer {token}"
        self._warp["action"]["description"] = f"Transfer {amount} {token}"
        
        data = {
            "token": token,
            "amount": amount
        }
        
        if recipient:
            data["recipient"] = recipient
        
        self._warp["action"]["data"] = data
        return self

    def swap_action(
        self,
        from_token: str,
        to_token: str,
        amount: str,
        min_amount_out: Optional[str] = None
    ) -> 'WarpBuilder':
        """Set a swap action.

        Args:
            from_token: Token to swap from
            to_token: Token to swap to
            amount: Amount to swap
            min_amount_out: Minimum amount to receive (optional)

        Returns:
            Self for chaining
        """
        self._warp["action"]["type"] = "swap"
        self._warp["action"]["title"] = f"Swap {from_token} to {to_token}"
        self._warp["action"]["description"] = f"Swap {amount} {from_token} to {to_token}"
        
        data = {
            "fromToken": from_token,
            "toToken": to_token,
            "amount": amount
        }
        
        if min_amount_out:
            data["minAmountOut"] = min_amount_out
        
        self._warp["action"]["data"] = data
        return self

    def nft_action(
        self,
        collection: str,
        token_id: str,
        action_type: str = "buy",
        price: Optional[str] = None
    ) -> 'WarpBuilder':
        """Set an NFT action.

        Args:
            collection: NFT collection
            token_id: Token ID
            action_type: Action type (buy, sell, transfer)
            price: Price (required for buy/sell)

        Returns:
            Self for chaining
        """
        self._warp["action"]["type"] = "nft"
        
        if action_type == "buy":
            self._warp["action"]["title"] = f"Buy NFT"
            self._warp["action"]["description"] = f"Buy NFT from collection {collection}"
        elif action_type == "sell":
            self._warp["action"]["title"] = f"Sell NFT"
            self._warp["action"]["description"] = f"Sell NFT from collection {collection}"
        else:  # transfer
            self._warp["action"]["title"] = f"Transfer NFT"
            self._warp["action"]["description"] = f"Transfer NFT from collection {collection}"
        
        data = {
            "collection": collection,
            "tokenId": token_id,
            "actionType": action_type
        }
        
        if price and action_type in ["buy", "sell"]:
            data["price"] = price
        
        self._warp["action"]["data"] = data
        return self

    def custom_action(
        self,
        action_type: str,
        title: str,
        description: str,
        data: Dict[str, Any]
    ) -> 'WarpBuilder':
        """Set a custom action.

        Args:
            action_type: Action type
            title: Action title
            description: Action description
            data: Action data

        Returns:
            Self for chaining
        """
        self._warp["action"]["type"] = action_type
        self._warp["action"]["title"] = title
        self._warp["action"]["description"] = description
        self._warp["action"]["data"] = data
        return self

    def build(self) -> Dict[str, Any]:
        """Build the Warp object.

        Returns:
            Warp object

        Raises:
            ValueError: If the Warp is invalid
        """
        # Set default values if not set
        if not self._warp["metadata"]["creator"] and self.config and self.config.user_address:
            self._warp["metadata"]["creator"] = self.config.user_address
        
        if not self._warp["metadata"]["createdAt"]:
            self._warp["metadata"]["createdAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        # Validate the Warp
        if not self.validator.validate_warp_schema(self._warp):
            raise ValueError("Invalid Warp schema")
        
        return self._warp

    def to_json(self) -> str:
        """Convert the Warp to JSON.

        Returns:
            Warp as JSON string
        """
        return json.dumps(self.build(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'WarpBuilder':
        """Create a WarpBuilder from JSON.

        Args:
            json_str: JSON string

        Returns:
            WarpBuilder instance

        Raises:
            ValueError: If the JSON is invalid
        """
        try:
            warp = json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")
        
        return cls.from_dict(warp)

    @classmethod
    def from_dict(cls, warp: Dict[str, Any]) -> 'WarpBuilder':
        """Create a WarpBuilder from a dictionary.

        Args:
            warp: Warp dictionary

        Returns:
            WarpBuilder instance
        """
        builder = cls()
        
        # Set basic properties
        if "name" in warp:
            builder.name(warp["name"])
        
        if "title" in warp:
            builder.title(warp["title"])
        
        if "description" in warp:
            builder.description(warp["description"])
        
        # Set action properties
        action = warp.get("action", {})
        
        if "type" in action:
            builder.action_type(action["type"])
        
        if "title" in action:
            builder.action_title(action["title"])
        
        if "description" in action:
            builder.action_description(action["description"])
        
        if "data" in action:
            builder.action_data(action["data"])
        
        # Set metadata properties
        metadata = warp.get("metadata", {})
        
        if "creator" in metadata:
            builder.creator(metadata["creator"])
        
        if "createdAt" in metadata:
            builder.created_at(metadata["createdAt"])
        
        return builder

    def create_inscription_transaction(self, warp: Dict[str, Any]) -> "Transaction":
        """Create an inscription transaction for the Warp.

        Args:
            warp: Warp object

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
            data="WARP-INSCRIPTION",
            gas_limit=50000,
            chain_id="D"
        )
