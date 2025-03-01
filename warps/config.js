require('dotenv').config();
const path = require('path');

// Warp configuration
const warpConfig = {
  env: process.env.MULTIVERSX_NETWORK || 'devnet',
  userAddress: process.env.WALLET_ADDRESS,
};

// Network provider configuration
const networkConfig = {
  apiUrl: process.env.MULTIVERSX_API_URL || 'https://devnet-api.multiversx.com',
  timeout: 10000,
  clientName: 'drawdash-warp'
};

// Contract addresses
const contractAddresses = {
  challenge: process.env.CHALLENGE_CONTRACT_ADDRESS,
  nft: process.env.NFT_CONTRACT_ADDRESS
};

// Wallet configuration
const walletConfig = {
  keystoreFile: process.env.WALLET_KEYSTORE_FILE ? path.resolve(__dirname, '..', process.env.WALLET_KEYSTORE_FILE) : undefined,
  password: process.env.WALLET_PASSWORD
};

// IPFS configuration (Pinata)
const ipfsConfig = {
  apiUrl: process.env.PINATA_API_URL,
  apiKey: process.env.PINATA_API_KEY,
  apiSecret: process.env.PINATA_API_SECRET
};

// Server configuration
const serverConfig = {
  port: process.env.PORT || 3000,
  host: process.env.HOST || 'localhost'
};

// AI services configuration
const aiConfig = {
  stabilityApiKey: process.env.STABILITY_API_KEY
};

module.exports = {
  warpConfig,
  networkConfig,
  contractAddresses,
  walletConfig,
  ipfsConfig,
  serverConfig,
  aiConfig
}; 