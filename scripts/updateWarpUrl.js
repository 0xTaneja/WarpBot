const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Check if a URL was provided
if (process.argv.length < 3) {
  console.error('Please provide a public URL as an argument');
  console.error('Example: node scripts/updateWarpUrl.js https://abc123.ngrok.io');
  process.exit(1);
}

const publicUrl = process.argv[2];
console.log(`Updating Warp actions to use public URL: ${publicUrl}`);

// Path to the deployWarp.js file
const deployWarpPath = path.join(__dirname, 'deployWarp.js');

// Read the deployWarp.js file
let deployWarpContent = fs.readFileSync(deployWarpPath, 'utf8');

// Replace all instances of http://localhost:3000 with the public URL
deployWarpContent = deployWarpContent.replace(/http:\/\/localhost:3000/g, publicUrl);

// Write the updated content back to the file
fs.writeFileSync(deployWarpPath, deployWarpContent);

console.log('Warp actions updated successfully');
console.log('To redeploy the Warp with the new URL, run:');
console.log('node scripts/deployWarp.js'); 