"""Action executor module for executing Warp actions."""

import json
import asyncio
from typing import Dict, Any, Optional, List, Union

from sdkwarp.config.models import Config
from sdkwarp.core.transaction.transaction import Transaction
from sdkwarp.core.transaction.signer import Signer
from sdkwarp.utils.validation import Validator
from sdkwarp.utils.encoding import encode_base64


class ActionExecutor:
    """Action executor for executing Warp actions."""

    def __init__(
        self,
        config: Config,
        signer: Optional[Signer] = None,
        validator: Optional[Validator] = None
    ):
        """Initialize the action executor.

        Args:
            config: SDK configuration
            signer: Signer instance
            validator: Validator instance
        """
        self.config = config
        self.signer = signer
        self.validator = validator or Validator()
        self._initialized = False

    async def init(self) -> None:
        """Initialize the action executor.

        Initializes the signer if provided.
        """
        if self.signer:
            await self.signer.init()
        
        self._initialized = True

    async def execute_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a Warp action.

        Args:
            action: Action to execute
            options: Additional options

        Returns:
            Execution result

        Raises:
            ValueError: If the action executor is not initialized or action is invalid
        """
        if not self._initialized:
            raise ValueError("Action executor not initialized. Call init() first.")
        
        # Validate action
        if not action or not isinstance(action, dict):
            raise ValueError("Invalid action: must be a non-empty dictionary")
        
        action_type = action.get("type")
        if not action_type:
            raise ValueError("Invalid action: missing 'type' field")
        
        # Execute action based on type
        if action_type == "transfer":
            return await self._execute_transfer_action(action, options)
        elif action_type == "swap":
            return await self._execute_swap_action(action, options)
        elif action_type == "stake":
            return await self._execute_stake_action(action, options)
        elif action_type == "nft":
            return await self._execute_nft_action(action, options)
        elif action_type == "custom":
            return await self._execute_custom_action(action, options)
        else:
            raise ValueError(f"Unsupported action type: {action_type}")

    async def _execute_transfer_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a transfer action.

        Args:
            action: Transfer action
            options: Additional options

        Returns:
            Execution result
        """
        # Validate action data
        data = action.get("data", {})
        if not data:
            raise ValueError("Invalid transfer action: missing 'data' field")
        
        token = data.get("token")
        if not token:
            raise ValueError("Invalid transfer action: missing 'token' field in data")
        
        amount = data.get("amount")
        if not amount:
            raise ValueError("Invalid transfer action: missing 'amount' field in data")
        
        recipient = data.get("recipient")
        if not recipient:
            raise ValueError("Invalid transfer action: missing 'recipient' field in data")
        
        # Validate recipient address
        if not self.validator.validate_address(recipient):
            raise ValueError(f"Invalid recipient address: {recipient}")
        
        # Create transaction based on token type
        if token.upper() == "EGLD":
            return await self._create_egld_transfer_transaction(recipient, amount, options)
        else:
            return await self._create_esdt_transfer_transaction(recipient, token, amount, options)

    async def _create_egld_transfer_transaction(
        self,
        recipient: str,
        amount: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an EGLD transfer transaction.

        Args:
            recipient: Recipient address
            amount: Amount to transfer
            options: Additional options

        Returns:
            Transaction result
        """
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Convert amount to atomic units (1 EGLD = 10^18 atomic units)
        try:
            # Handle decimal amounts
            if "." in amount:
                whole, fraction = amount.split(".")
                # Pad fraction with zeros to 18 decimal places
                fraction = fraction.ljust(18, "0")[:18]
                atomic_amount = whole + fraction
            else:
                atomic_amount = amount + "0" * 18
            
            # Remove leading zeros
            atomic_amount = atomic_amount.lstrip("0")
            if not atomic_amount:
                atomic_amount = "0"
        except Exception as e:
            raise ValueError(f"Failed to convert amount to atomic units: {e}")
        
        # Create transaction
        transaction = Transaction(
            sender=self.config.user_address,
            receiver=recipient,
            value=atomic_amount,
            data="",
            gas_limit=50000,
            chain_id=self.config.chain_id or "D"
        )
        
        # In a real implementation, this would send the transaction to the blockchain
        # For now, return a dummy result
        return {
            "status": "success",
            "transaction": transaction.to_dict(),
            "hash": "dummy_transaction_hash"
        }

    async def _create_esdt_transfer_transaction(
        self,
        recipient: str,
        token: str,
        amount: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an ESDT transfer transaction.

        Args:
            recipient: Recipient address
            token: Token identifier
            amount: Amount to transfer
            options: Additional options

        Returns:
            Transaction result
        """
        if not self.config.user_address:
            raise ValueError("User address not set in configuration")
        
        # Convert amount to atomic units (assuming 18 decimals for simplicity)
        try:
            # Handle decimal amounts
            if "." in amount:
                whole, fraction = amount.split(".")
                # Pad fraction with zeros to 18 decimal places
                fraction = fraction.ljust(18, "0")[:18]
                atomic_amount = whole + fraction
            else:
                atomic_amount = amount + "0" * 18
            
            # Remove leading zeros
            atomic_amount = atomic_amount.lstrip("0")
            if not atomic_amount:
                atomic_amount = "0"
        except Exception as e:
            raise ValueError(f"Failed to convert amount to atomic units: {e}")
        
        # Create function call data
        data = f"ESDTTransfer@{encode_base64(token)}@{encode_base64(atomic_amount)}"
        
        # Create transaction
        transaction = Transaction(
            sender=self.config.user_address,
            receiver=recipient,
            value="0",
            data=data,
            gas_limit=500000,
            chain_id=self.config.chain_id or "D"
        )
        
        # In a real implementation, this would send the transaction to the blockchain
        # For now, return a dummy result
        return {
            "status": "success",
            "transaction": transaction.to_dict(),
            "hash": "dummy_transaction_hash"
        }

    async def _execute_swap_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a swap action.

        Args:
            action: Swap action
            options: Additional options

        Returns:
            Execution result
        """
        # In a real implementation, this would execute a swap action
        # For now, return a dummy result
        return {
            "status": "success",
            "message": "Swap action executed",
            "hash": "dummy_transaction_hash"
        }

    async def _execute_stake_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a stake action.

        Args:
            action: Stake action
            options: Additional options

        Returns:
            Execution result
        """
        # In a real implementation, this would execute a stake action
        # For now, return a dummy result
        return {
            "status": "success",
            "message": "Stake action executed",
            "hash": "dummy_transaction_hash"
        }

    async def _execute_nft_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute an NFT action.

        Args:
            action: NFT action
            options: Additional options

        Returns:
            Execution result
        """
        # In a real implementation, this would execute an NFT action
        # For now, return a dummy result
        return {
            "status": "success",
            "message": "NFT action executed",
            "hash": "dummy_transaction_hash"
        }

    async def _execute_custom_action(
        self,
        action: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a custom action.

        Args:
            action: Custom action
            options: Additional options

        Returns:
            Execution result
        """
        # In a real implementation, this would execute a custom action
        # For now, return a dummy result
        return {
            "status": "success",
            "message": "Custom action executed",
            "hash": "dummy_transaction_hash"
        } 