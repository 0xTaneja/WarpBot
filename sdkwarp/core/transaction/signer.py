"""Signer module for signing transactions."""

import json
import hashlib
from typing import Dict, Any, Optional, Union

from sdkwarp.config.models import Config
from sdkwarp.core.transaction.transaction import Transaction
from sdkwarp.utils.encoding import encode_hex, decode_hex


class Signer:
    """Signer for signing transactions."""

    def __init__(self, config: Config):
        """Initialize the signer.

        Args:
            config: SDK configuration
        """
        self.config = config
        self._initialized = False
        self._wallet_key = None

    async def init(self) -> None:
        """Initialize the signer.

        Loads wallet key if available in the configuration.
        """
        if self.config.wallet_key:
            self._wallet_key = self.config.wallet_key
            self._initialized = True
        elif self.config.wallet_pem_file:
            await self._load_pem_file(self.config.wallet_pem_file)
            self._initialized = True
        elif self.config.wallet_keystore_file and self.config.wallet_password:
            await self._load_keystore_file(
                self.config.wallet_keystore_file,
                self.config.wallet_password
            )
            self._initialized = True

    async def _load_pem_file(self, pem_file: str) -> None:
        """Load wallet key from PEM file.

        Args:
            pem_file: Path to PEM file

        Raises:
            ValueError: If the PEM file is invalid
        """
        # In a real implementation, this would load the key from the PEM file
        # For now, set a dummy key
        self._wallet_key = "dummy_key_from_pem"

    async def _load_keystore_file(self, keystore_file: str, password: str) -> None:
        """Load wallet key from keystore file.

        Args:
            keystore_file: Path to keystore file
            password: Keystore password

        Raises:
            ValueError: If the keystore file is invalid or password is incorrect
        """
        # In a real implementation, this would load the key from the keystore file
        # For now, set a dummy key
        self._wallet_key = "dummy_key_from_keystore"

    def sign_transaction(self, transaction: Transaction) -> str:
        """Sign a transaction.

        Args:
            transaction: Transaction to sign

        Returns:
            Transaction signature

        Raises:
            ValueError: If the signer is not initialized
        """
        if not self._initialized:
            raise ValueError("Signer not initialized. Call init() first.")
        
        if not self._wallet_key:
            raise ValueError("Wallet key not available")
        
        # In a real implementation, this would sign the transaction using the wallet key
        # For now, return a dummy signature
        tx_json = transaction.to_json()
        tx_hash = hashlib.sha256(tx_json.encode()).hexdigest()
        return f"dummy_signature_{tx_hash}"

    def sign_message(self, message: Union[str, bytes]) -> str:
        """Sign a message.

        Args:
            message: Message to sign

        Returns:
            Message signature

        Raises:
            ValueError: If the signer is not initialized
        """
        if not self._initialized:
            raise ValueError("Signer not initialized. Call init() first.")
        
        if not self._wallet_key:
            raise ValueError("Wallet key not available")
        
        # In a real implementation, this would sign the message using the wallet key
        # For now, return a dummy signature
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        message_hash = hashlib.sha256(message).hexdigest()
        return f"dummy_signature_{message_hash}"

    def verify_signature(
        self,
        message: Union[str, bytes],
        signature: str,
        address: Optional[str] = None
    ) -> bool:
        """Verify a signature.

        Args:
            message: Original message
            signature: Signature to verify
            address: Address that signed the message (if None, uses the configured address)

        Returns:
            True if the signature is valid, False otherwise

        Raises:
            ValueError: If the address is not provided and not available in the configuration
        """
        if not address and not self.config.user_address:
            raise ValueError("Address not provided and not available in configuration")
        
        address = address or self.config.user_address
        
        # In a real implementation, this would verify the signature
        # For now, return True for dummy signatures
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        message_hash = hashlib.sha256(message).hexdigest()
        expected_signature = f"dummy_signature_{message_hash}"
        
        return signature == expected_signature
