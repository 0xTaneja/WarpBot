"""Transaction execution for the SDK."""

import asyncio
from typing import Any, Dict, Optional, Union

from sdkwarp.config.models import Config
from sdkwarp.core.transaction.signer import Signer
from sdkwarp.core.transaction.arg_serializer import ArgSerializer
from sdkwarp.utils.validation import Validator


class ActionExecutor:
    """Executes actions on the blockchain."""

    def __init__(
        self,
        config: Config,
        signer: Optional[Signer] = None,
        serializer: Optional[ArgSerializer] = None,
        validator: Optional[Validator] = None
    ):
        """Initialize the action executor.

        Args:
            config: SDK configuration
            signer: Transaction signer
            serializer: Argument serializer
            validator: Validator instance
        """
        self.config = config
        self.signer = signer or Signer(config)
        self.serializer = serializer or ArgSerializer()
        self.validator = validator or Validator()
        self._initialized = False
    
    async def init(self) -> None:
        """Initialize the action executor.

        Returns:
            None
        """
        if not self._initialized:
            await self.signer.init()
            self._initialized = True
    
    async def execute_action(
        self,
        action_type: str,
        action_data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute an action on the blockchain.

        Args:
            action_type: Type of action to execute
            action_data: Action data
            options: Transaction options

        Returns:
            Transaction result

        Raises:
            ValueError: If the action type is invalid
            RuntimeError: If the executor is not initialized
        """
        if not self._initialized:
            raise RuntimeError("ActionExecutor is not initialized")
        
        if not self.validator.validate_action_type(action_type):
            raise ValueError(f"Invalid action type: {action_type}")
        
        # Get the appropriate handler for the action type
        action_handler = self._get_action_handler(action_type)
        
        # Execute the action
        return await action_handler(action_data, options or {})
    
    def _get_action_handler(self, action_type: str):
        """Get the handler for the specified action type.

        Args:
            action_type: Type of action

        Returns:
            Action handler function
        
        Raises:
            ValueError: If the action type is not supported
        """
        action_handlers = {
            "transfer": self._handle_transfer_action,
            "swap": self._handle_swap_action,
            "nft": self._handle_nft_action,
            "custom": self._handle_custom_action,
        }
        
        if action_type not in action_handlers:
            raise ValueError(f"Unsupported action type: {action_type}")
        
        return action_handlers[action_type]
    
    async def _handle_transfer_action(
        self,
        action_data: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a transfer action.

        Args:
            action_data: Transfer data
            options: Transaction options

        Returns:
            Transaction result
        """
        # Validate transfer data
        if not self.validator.validate_transfer_data(action_data):
            raise ValueError("Invalid transfer data")
        
        # Create transaction
        tx_data = {
            "receiver": action_data.get("receiver"),
            "value": action_data.get("value", "0"),
            "data": self.serializer.serialize_transfer_data(action_data),
        }
        
        # Sign and send the transaction
        tx_hash = await self.signer.sign_and_send_transaction(tx_data, options)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "action_type": "transfer",
            "action_data": action_data
        }
    
    async def _handle_swap_action(
        self,
        action_data: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a swap action.

        Args:
            action_data: Swap data
            options: Transaction options

        Returns:
            Transaction result
        """
        # Validate swap data
        if not self.validator.validate_swap_data(action_data):
            raise ValueError("Invalid swap data")
        
        # Create transaction
        tx_data = {
            "receiver": action_data.get("swap_contract"),
            "value": action_data.get("value", "0"),
            "data": self.serializer.serialize_swap_data(action_data),
        }
        
        # Sign and send the transaction
        tx_hash = await self.signer.sign_and_send_transaction(tx_data, options)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "action_type": "swap",
            "action_data": action_data
        }
    
    async def _handle_nft_action(
        self,
        action_data: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle an NFT action.

        Args:
            action_data: NFT data
            options: Transaction options

        Returns:
            Transaction result
        """
        # Validate NFT data
        if not self.validator.validate_nft_data(action_data):
            raise ValueError("Invalid NFT data")
        
        # Create transaction
        tx_data = {
            "receiver": action_data.get("nft_contract"),
            "value": action_data.get("value", "0"),
            "data": self.serializer.serialize_nft_data(action_data),
        }
        
        # Sign and send the transaction
        tx_hash = await self.signer.sign_and_send_transaction(tx_data, options)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "action_type": "nft",
            "action_data": action_data
        }
    
    async def _handle_custom_action(
        self,
        action_data: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a custom action.

        Args:
            action_data: Custom action data
            options: Transaction options

        Returns:
            Transaction result
        """
        # Validate custom action data
        if not self.validator.validate_custom_data(action_data):
            raise ValueError("Invalid custom action data")
        
        # Create transaction
        tx_data = {
            "receiver": action_data.get("contract"),
            "value": action_data.get("value", "0"),
            "data": action_data.get("data", ""),
        }
        
        # Sign and send the transaction
        tx_hash = await self.signer.sign_and_send_transaction(tx_data, options)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "action_type": "custom",
            "action_data": action_data
        }
