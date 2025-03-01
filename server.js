const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { handleWarpRequest } = require('./warps/warpExecutor');
const { serverConfig } = require('./warps/config');
const path = require('path');
const fs = require('fs');

// Create Express app
const app = express();

// Middleware
app.use(cors({
  origin: ['https://devnet.usewarp.to', 'http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));
// Serve static files from the frontend directory
app.use('/frontend', express.static(path.join(__dirname, 'frontend')));

// Create temp directory if it doesn't exist
const tempDir = path.join(__dirname, 'temp');
if (!fs.existsSync(tempDir)) {
  fs.mkdirSync(tempDir, { recursive: true });
}

// Create public directory if it doesn't exist
const publicDir = path.join(__dirname, 'public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

// Root route - serve the index.html file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Drawing canvas demo route
app.get('/drawing-canvas', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'DrawDash server is running' });
});

// Warp execution endpoint
app.post('/warp', async (req, res) => {
  try {
    console.log('Received Warp request:', req.body);
    
    const result = await handleWarpRequest(req.body);
    
    res.status(result.success ? 200 : 400).json(result);
  } catch (error) {
    console.error('Error handling Warp request:', error);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
      data: null
    });
  }
});

// Action-specific endpoints for direct API access
app.post('/api/challenge/create', async (req, res) => {
  try {
    const result = await handleWarpRequest({
      action: 'createChallenge',
      args: req.body
    });
    
    res.status(result.success ? 200 : 400).json(result);
  } catch (error) {
    console.error('Error creating challenge:', error);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
      data: null
    });
  }
});

app.post('/api/drawing/submit', async (req, res) => {
  try {
    const result = await handleWarpRequest({
      action: 'submitDrawing',
      args: req.body
    });
    
    res.status(result.success ? 200 : 400).json(result);
  } catch (error) {
    console.error('Error submitting drawing:', error);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
      data: null
    });
  }
});

app.post('/api/nft/mint', async (req, res) => {
  try {
    const result = await handleWarpRequest({
      action: 'mintNFT',
      args: req.body
    });
    
    res.status(result.success ? 200 : 400).json(result);
  } catch (error) {
    console.error('Error minting NFT:', error);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
      data: null
    });
  }
});

app.get('/api/user/stats/:userAddress', async (req, res) => {
  try {
    const result = await handleWarpRequest({
      action: 'getUserStats',
      args: {
        userAddress: req.params.userAddress
      }
    });
    
    res.status(result.success ? 200 : 400).json(result);
  } catch (error) {
    console.error('Error getting user stats:', error);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
      data: null
    });
  }
});

// Start the server
const PORT = serverConfig.port || 3000;
const HOST = serverConfig.host || 'localhost';

app.listen(PORT, HOST, () => {
  console.log(`DrawDash server running at http://${HOST}:${PORT}`);
  console.log(`Health check: http://${HOST}:${PORT}/health`);
  console.log(`Warp endpoint: http://${HOST}:${PORT}/warp`);
}); 