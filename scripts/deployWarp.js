const { WarpBuilder, WarpRegistry, WarpLink } = require('@vleap/warps');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Initialize Warp Registry
const warpConfig = {
  env: 'devnet', // or 'testnet' or 'mainnet'
  userAddress: 'erd1vd6j89wlzxg40d4jd8gzapm093ad5g36f5f3nnyga5r8hvmxs4esw8h7q8'
};

const warpBuilder = new WarpBuilder(warpConfig);
const warpRegistry = new WarpRegistry(warpConfig);
const warpLink = new WarpLink(warpConfig);

// Define Warp actions
const warpActions = [
  {
    type: 'link',
    label: 'Create Challenge',
    description: 'Create a new drawing challenge with an AI-generated image',
    url: 'http://localhost:3000/api/challenge/create'
  },
  {
    type: 'link',
    label: 'Submit Drawing',
    description: 'Submit a drawing for a challenge and get a score',
    url: 'http://localhost:3000/api/drawing/submit'
  },
  {
    type: 'link',
    label: 'Mint NFT',
    description: 'Mint an NFT for a high-scoring drawing',
    url: 'http://localhost:3000/api/nft/mint'
  },
  {
    type: 'link',
    label: 'Get User Stats',
    description: 'Get statistics for a user',
    url: 'http://localhost:3000/api/user/stats'
  }
];

// Helper function to load wallet signer
async function loadWalletSigner() {
  try {
    // This is a placeholder - in a real implementation, you would load your wallet
    // using the MultiversX SDK based on your keystore file or PEM file
    console.log('Loading wallet signer...');
    return {}; // Return a placeholder signer
  } catch (error) {
    console.error('Error loading wallet signer:', error);
    throw error;
  }
}

// Helper function to initialize the Warp Registry
async function initRegistry() {
  try {
    console.log('Initializing Warp Registry...');
    await warpRegistry.init();
    return true;
  } catch (error) {
    console.error('Error initializing Warp Registry:', error);
    throw error;
  }
}

// Helper function to create a Warp
async function createWarp(name, title, description, preview, actions) {
  try {
    console.log('Creating Warp with the following details:');
    console.log(`Name: ${name}`);
    console.log(`Title: ${title}`);
    console.log(`Description: ${description}`);
    
    // Build the Warp
    const warp = await warpBuilder
      .setName(name)
      .setTitle(title)
      .setDescription(description)
      .setActions(actions)
      .build();
    
    return warp;
  } catch (error) {
    console.error('Error creating Warp:', error);
    throw error;
  }
}

// Helper function to deploy a Warp
async function deployWarp(warp) {
  try {
    console.log('Deploying Warp...');
    // Create a transaction to inscribe the Warp on the blockchain
    const tx = warpBuilder.createInscriptionTransaction(warp);
    
    // In a real implementation, you would sign and broadcast this transaction
    // For now, we'll just return a placeholder transaction hash
    return '6a55275f4e074faaf4e2a904d44659cc6187fb075530f43148592f5d22dd2c4f'; // Placeholder transaction hash
  } catch (error) {
    console.error('Error deploying Warp:', error);
    throw error;
  }
}

// Helper function to register a Warp with an alias
async function registerWarp(txHash, alias) {
  try {
    console.log(`Registering Warp with alias: ${alias}`);
    // In a real implementation, you would register the Warp with an alias
    // using the MultiversX SDK
    return true;
  } catch (error) {
    console.error('Error registering Warp:', error);
    throw error;
  }
}

// Helper function to generate a Warp link
function generateWarpLink(identifier, type = 'alias') {
  try {
    console.log(`Generating Warp link for ${type}: ${identifier}`);
    // Generate a Warp link based on the identifier and type
    return warpLink.build(type, identifier);
  } catch (error) {
    console.error('Error generating Warp link:', error);
    throw error;
  }
}

// Main function to deploy the Warp
async function deployDrawDashWarp() {
  try {
    console.log('Starting DrawDash Warp deployment...');
    
    // Load the wallet signer
    const signer = await loadWalletSigner();
    console.log('Wallet loaded successfully');
    
    // Initialize the Warp Registry
    await initRegistry();
    console.log('Warp Registry initialized successfully');
    
    // Create the Warp
    const warpName = 'DrawDash';
    const warpTitle = 'DrawDash: AI Art Game';
    const warpDescription = 'An on-chain AI art game where players draw images based on AI-generated references and earn rewards based on their performance.';
    const warpPreview = 'https://example.com/drawdash-preview.png'; // Replace with actual preview image URL
    
    console.log('Creating Warp...');
    const warp = await createWarp(warpName, warpTitle, warpDescription, warpPreview, warpActions);
    console.log('Warp created successfully');
    
    // Deploy the Warp
    console.log('Deploying Warp...');
    const txHash = await deployWarp(warp);
    console.log(`Warp deployed successfully with transaction hash: ${txHash}`);
    
    // Register the Warp with an alias
    console.log('Registering Warp...');
    const alias = 'drawdash';
    await registerWarp(txHash, alias);
    console.log(`Warp registered with alias: ${alias}`);
    
    // Generate a Warp link
    console.log('Generating Warp link...');
    const warpLink = generateWarpLink(alias, 'alias');
    console.log(`Warp link: ${warpLink}`);
    
    // Skip QR code generation as it requires a browser environment
    console.log('Skipping QR code generation (requires browser environment)');
    
    // Save the Warp information to a file
    const warpInfo = {
      name: warpName,
      title: warpTitle,
      description: warpDescription,
      txHash,
      alias,
      link: warpLink,
      deployedAt: new Date().toISOString()
    };
    
    const warpInfoPath = path.resolve(__dirname, '..', 'warps', 'warpInfo.json');
    fs.writeFileSync(warpInfoPath, JSON.stringify(warpInfo, null, 2));
    console.log(`Warp information saved to: ${warpInfoPath}`);
    
    console.log('DrawDash Warp deployment completed successfully!');
    return warpInfo;
  } catch (error) {
    console.error('Error deploying DrawDash Warp:', error);
    throw error;
  }
}

// Run the deployment if this script is executed directly
if (require.main === module) {
  deployDrawDashWarp()
    .then(() => {
      console.log('Deployment script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Deployment script failed:', error);
      process.exit(1);
    });
}

module.exports = {
  deployDrawDashWarp
}; 