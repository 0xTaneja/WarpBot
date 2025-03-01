const { executeWarpAction } = require('../warps/warpExecutor');
const fs = require('fs');
const path = require('path');

// Test the createChallenge action
async function testCreateChallenge() {
  console.log('Testing createChallenge action...');
  
  const result = await executeWarpAction('createChallenge', {
    prompt: 'A colorful abstract painting with geometric shapes'
  });
  
  console.log('createChallenge result:', JSON.stringify(result, null, 2));
  return result;
}

// Test the submitDrawing action
async function testSubmitDrawing(challengeId) {
  console.log('Testing submitDrawing action...');
  
  // For testing, we'll use a sample base64 image
  // In a real scenario, this would be the user's drawing
  const sampleDrawingPath = path.resolve(__dirname, '..', 'public', 'sample-drawing.txt');
  let drawingData;
  
  if (fs.existsSync(sampleDrawingPath)) {
    drawingData = fs.readFileSync(sampleDrawingPath, 'utf8');
  } else {
    // Create a simple placeholder if the file doesn't exist
    drawingData = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    fs.writeFileSync(sampleDrawingPath, drawingData);
  }
  
  const result = await executeWarpAction('submitDrawing', {
    drawingData,
    challengeId
  });
  
  console.log('submitDrawing result:', JSON.stringify(result, null, 2));
  return result;
}

// Test the mintNFT action
async function testMintNFT(challengeId, score) {
  console.log('Testing mintNFT action...');
  
  // For testing, we'll use a sample base64 image
  const sampleDrawingPath = path.resolve(__dirname, '..', 'public', 'sample-drawing.txt');
  let drawingData;
  
  if (fs.existsSync(sampleDrawingPath)) {
    drawingData = fs.readFileSync(sampleDrawingPath, 'utf8');
  } else {
    // Create a simple placeholder if the file doesn't exist
    drawingData = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    fs.writeFileSync(sampleDrawingPath, drawingData);
  }
  
  const result = await executeWarpAction('mintNFT', {
    drawingData,
    challengeId,
    score: score || 85 // Default to a high score for testing
  });
  
  console.log('mintNFT result:', JSON.stringify(result, null, 2));
  return result;
}

// Test the getUserStats action
async function testGetUserStats() {
  console.log('Testing getUserStats action...');
  
  const result = await executeWarpAction('getUserStats', {
    userAddress: 'erd1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
  });
  
  console.log('getUserStats result:', JSON.stringify(result, null, 2));
  return result;
}

// Run all tests
async function runAllTests() {
  try {
    console.log('Starting Warp integration tests...');
    
    // Test createChallenge
    const challengeResult = await testCreateChallenge();
    const challengeId = challengeResult.data?.challengeId;
    
    if (challengeId) {
      // Test submitDrawing
      const drawingResult = await testSubmitDrawing(challengeId);
      const score = drawingResult.data?.score;
      
      // Test mintNFT
      if (score) {
        await testMintNFT(challengeId, score);
      }
    }
    
    // Test getUserStats
    await testGetUserStats();
    
    console.log('All tests completed successfully!');
  } catch (error) {
    console.error('Error running tests:', error);
  }
}

// Run the tests if this script is executed directly
if (require.main === module) {
  runAllTests()
    .then(() => {
      console.log('Test script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Test script failed:', error);
      process.exit(1);
    });
}

module.exports = {
  testCreateChallenge,
  testSubmitDrawing,
  testMintNFT,
  testGetUserStats,
  runAllTests
}; 