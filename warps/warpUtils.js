const { WarpBuilder, WarpRegistry, WarpLink } = require('@vleap/warps');
const { UserSigner } = require('@multiversx/sdk-wallet');
const { ApiNetworkProvider } = require('@multiversx/sdk-network-providers');
const { Address } = require('@multiversx/sdk-core');
const fs = require('fs');
const path = require('path');
const { warpConfig, networkConfig, walletConfig } = require('./config');

// Initialize Warp components
const warpBuilder = new WarpBuilder(warpConfig);
const warpRegistry = new WarpRegistry(warpConfig);
const warpLink = new WarpLink(warpConfig);

// Initialize network provider
const provider = new ApiNetworkProvider(networkConfig.apiUrl, {
  timeout: networkConfig.timeout,
  clientName: networkConfig.clientName
});

// Function to load wallet signer
async function loadWalletSigner() {
  try {
    if (!walletConfig.keystoreFile) {
      throw new Error('Wallet keystore file path not provided');
    }
    
    const keystoreContent = fs.readFileSync(walletConfig.keystoreFile, { encoding: 'utf8' });
    const keystoreObj = JSON.parse(keystoreContent);
    const userSigner = UserSigner.fromWallet(keystoreObj, walletConfig.password);
    console.log('Wallet loaded successfully');
    return userSigner;
  } catch (error) {
    console.error('Error loading wallet:', error);
    throw error;
  }
}

// Initialize the registry
async function initRegistry() {
  try {
    await warpRegistry.init();
    console.log('Warp Registry initialized successfully');
  } catch (error) {
    console.error('Error initializing Warp Registry:', error);
    throw error;
  }
}

// Create a Warp
async function createWarp(name, title, description, preview, actions) {
  try {
    // Build the Warp
    const warp = await warpBuilder
      .setName(name)
      .setTitle(title)
      .setDescription(description)
      .setPreview(preview)
      .setActions(actions)
      .build();
    
    console.log('Warp created successfully!');
    return warp;
  } catch (error) {
    console.error('Error creating Warp:', error);
    throw error;
  }
}

// Deploy a Warp to the blockchain
async function deployWarp(warp) {
  try {
    // Create a transaction to inscribe the Warp on the blockchain
    const tx = warpBuilder.createInscriptionTransaction(warp);
    
    // Load the signer
    const signer = await loadWalletSigner();
    
    // Get the user address
    const userAddress = new Address(warpConfig.userAddress);
    
    // Get the current account nonce
    const account = await provider.getAccount(userAddress);
    let currentNonce = account.nonce;
    
    // Set the nonce for the transaction
    tx.nonce = currentNonce++;
    
    // Sign the transaction
    const signedTx = tx.serializeForSigning();
    const signature = await signer.sign(signedTx);
    tx.applySignature(signature);
    
    // Send the transaction
    const txHash = await provider.sendTransaction(tx);
    console.log(`Transaction sent! Hash: ${txHash}`);
    
    // Wait for the transaction to be confirmed
    await new Promise(resolve => setTimeout(resolve, 15000)); // Wait 15 seconds
    
    return txHash;
  } catch (error) {
    console.error('Error deploying Warp:', error);
    throw error;
  }
}

// Register a Warp with an alias
async function registerWarp(txHash, alias) {
  try {
    // Load the signer
    const signer = await loadWalletSigner();
    
    // Get the user address
    const userAddress = new Address(warpConfig.userAddress);
    
    // Get the current account nonce
    const account = await provider.getAccount(userAddress);
    let currentNonce = account.nonce;
    
    // Create a transaction to register the Warp
    const registerTx = warpRegistry.createWarpRegisterTransaction(txHash, alias);
    
    // Set the nonce for the transaction
    registerTx.nonce = currentNonce++;
    
    // Sign the transaction
    const signedRegisterTx = registerTx.serializeForSigning();
    const registerSignature = await signer.sign(signedRegisterTx);
    registerTx.applySignature(registerSignature);
    
    // Send the transaction
    const registerTxHash = await provider.sendTransaction(registerTx);
    console.log(`Warp registered! Registration transaction hash: ${registerTxHash}`);
    
    return { txHash, alias, registerTxHash };
  } catch (error) {
    console.error('Error registering Warp:', error);
    throw error;
  }
}

// Generate a shareable link for a Warp
function generateWarpLink(id, type = 'alias') {
  try {
    const warpUrl = warpLink.build(type, id);
    console.log(`Warp link generated: ${warpUrl}`);
    return warpUrl;
  } catch (error) {
    console.error('Error generating Warp link:', error);
    throw error;
  }
}

// Generate a QR code for a Warp
async function generateWarpQR(id, type = 'alias', outputPath) {
  try {
    const qrCode = warpLink.generateQrCode(type, id);
    
    // Get the QR code as SVG
    const qrSvg = await qrCode.getRawData('svg');
    
    // Save the QR code to a file
    const filePath = outputPath || path.resolve(__dirname, '..', 'warp-qrcode.svg');
    fs.writeFileSync(filePath, qrSvg);
    console.log(`QR code saved to ${filePath}`);
    
    return { qrCode, filePath };
  } catch (error) {
    console.error('Error generating Warp QR code:', error);
    throw error;
  }
}

// Get information about a Warp by its hash
async function getWarpByHash(hash) {
  try {
    // Get the Warp from the blockchain
    const warp = await warpBuilder.createFromTransactionHash(hash);
    
    // Get registry information
    const { registryInfo, brand } = await warpRegistry.getInfoByHash(hash);
    
    return { warp, registryInfo, brand };
  } catch (error) {
    console.error('Error getting Warp by hash:', error);
    throw error;
  }
}

// Get information about a Warp by its alias
async function getWarpByAlias(alias) {
  try {
    // Get registry information
    const { registryInfo, brand } = await warpRegistry.getInfoByAlias(alias);
    
    // If we have registry info, get the Warp using the hash
    let warp = null;
    if (registryInfo) {
      warp = await warpBuilder.createFromTransactionHash(registryInfo.hash);
    }
    
    return { warp, registryInfo, brand };
  } catch (error) {
    console.error('Error getting Warp by alias:', error);
    throw error;
  }
}

module.exports = {
  warpBuilder,
  warpRegistry,
  warpLink,
  provider,
  loadWalletSigner,
  initRegistry,
  createWarp,
  deployWarp,
  registerWarp,
  generateWarpLink,
  generateWarpQR,
  getWarpByHash,
  getWarpByAlias
}; 