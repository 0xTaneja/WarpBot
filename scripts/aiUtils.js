const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { aiConfig } = require('../warps/config');
const { ipfsConfig } = require('../warps/config');
const FormData = require('form-data');

// Generate an image from a text prompt using Stability AI
async function generateImageFromPrompt(prompt) {
  try {
    if (!aiConfig.stabilityApiKey) {
      throw new Error('Stability API key not provided');
    }

    console.log(`Generating image for prompt: "${prompt}"`);
    
    const response = await axios({
      method: 'post',
      url: 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${aiConfig.stabilityApiKey}`
      },
      data: {
        text_prompts: [
          {
            text: prompt,
            weight: 1
          }
        ],
        cfg_scale: 7,
        height: 1024,
        width: 1024,
        samples: 1,
        steps: 30
      }
    });

    if (response.data && response.data.artifacts && response.data.artifacts.length > 0) {
      const base64Image = response.data.artifacts[0].base64;
      console.log('Image generated successfully');
      return base64Image;
    } else {
      throw new Error('No image generated from the API');
    }
  } catch (error) {
    console.error('Error generating image:', error.response ? error.response.data : error.message);
    throw error;
  }
}

// Save a base64 image to a file
function saveBase64Image(base64Image, outputPath) {
  try {
    const imageBuffer = Buffer.from(base64Image, 'base64');
    fs.writeFileSync(outputPath, imageBuffer);
    console.log(`Image saved to ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error('Error saving image:', error);
    throw error;
  }
}

// Upload an image to IPFS using Pinata
async function uploadImageToIPFS(imagePath) {
  try {
    if (!ipfsConfig.apiKey || !ipfsConfig.apiSecret) {
      throw new Error('Pinata API credentials not provided');
    }

    console.log(`Uploading image to IPFS: ${imagePath}`);
    
    // Create a form data object
    const formData = new FormData();
    
    // Add the file to the form data
    const fileStream = fs.createReadStream(imagePath);
    formData.append('file', fileStream);
    
    // Add metadata
    const metadata = JSON.stringify({
      name: `DrawDash-${Date.now()}`,
      keyvalues: {
        app: 'DrawDash',
        timestamp: Date.now().toString()
      }
    });
    formData.append('pinataMetadata', metadata);
    
    // Add options
    const options = JSON.stringify({
      cidVersion: 0
    });
    formData.append('pinataOptions', options);
    
    // Upload to Pinata
    const response = await axios.post(
      `${ipfsConfig.apiUrl}/pinning/pinFileToIPFS`,
      formData,
      {
        headers: {
          'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
          'pinata_api_key': ipfsConfig.apiKey,
          'pinata_secret_api_key': ipfsConfig.apiSecret
        }
      }
    );
    
    const ipfsHash = response.data.IpfsHash;
    console.log(`Image uploaded to IPFS with hash: ${ipfsHash}`);
    return ipfsHash;
  } catch (error) {
    console.error('Error uploading to IPFS:', error.response ? error.response.data : error.message);
    throw error;
  }
}

// Upload a base64 image directly to IPFS using Pinata
async function uploadBase64ImageToIPFS(base64Image) {
  try {
    if (!ipfsConfig.apiKey || !ipfsConfig.apiSecret) {
      throw new Error('Pinata API credentials not provided');
    }
    
    // Convert base64 to buffer
    const imageBuffer = Buffer.from(base64Image, 'base64');
    
    // Create a temporary file
    const tempFilePath = path.resolve(__dirname, '..', 'temp', `${Date.now()}.png`);
    
    // Make sure the temp directory exists
    const tempDir = path.resolve(__dirname, '..', 'temp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    
    // Save the buffer to the temporary file
    fs.writeFileSync(tempFilePath, imageBuffer);
    
    // Upload the file to IPFS
    const ipfsHash = await uploadImageToIPFS(tempFilePath);
    
    // Clean up the temporary file
    fs.unlinkSync(tempFilePath);
    
    return ipfsHash;
  } catch (error) {
    console.error('Error uploading to IPFS:', error);
    throw error;
  }
}

// Calculate similarity score between two images
// Note: This is a placeholder. In a real implementation, you would use a computer vision API
async function calculateImageSimilarity(referenceImageUrl, userDrawingUrl) {
  try {
    console.log(`Calculating similarity between ${referenceImageUrl} and ${userDrawingUrl}`);
    
    // This is a placeholder. In a real implementation, you would call a computer vision API
    // For now, we'll return a random score between 50 and 100
    const similarityScore = Math.floor(Math.random() * 51) + 50;
    
    console.log(`Similarity score: ${similarityScore}`);
    return similarityScore;
  } catch (error) {
    console.error('Error calculating image similarity:', error);
    throw error;
  }
}

// Generate a complete challenge
async function generateChallenge(prompt) {
  try {
    // Generate the image
    const base64Image = await generateImageFromPrompt(prompt);
    
    // Save the image to a temporary file
    const tempImagePath = path.resolve(__dirname, '..', 'temp', `${Date.now()}.png`);
    
    // Make sure the temp directory exists
    const tempDir = path.resolve(__dirname, '..', 'temp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    
    saveBase64Image(base64Image, tempImagePath);
    
    // Upload the image to IPFS
    const ipfsHash = await uploadImageToIPFS(tempImagePath);
    
    // Return the challenge data
    return {
      prompt,
      imageBase64: base64Image,
      imagePath: tempImagePath,
      ipfsHash,
      ipfsUrl: `ipfs://${ipfsHash}`
    };
  } catch (error) {
    console.error('Error generating challenge:', error);
    throw error;
  }
}

module.exports = {
  generateImageFromPrompt,
  saveBase64Image,
  uploadImageToIPFS,
  uploadBase64ImageToIPFS,
  calculateImageSimilarity,
  generateChallenge
}; 