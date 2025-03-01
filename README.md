# DrawDash: AI Art Game

DrawDash is an on-chain AI art game where players draw images based on AI-generated references and earn rewards based on their performance. The game is integrated with the MultiversX blockchain using the Warp Protocol.

## Features

- Create drawing challenges with AI-generated reference images
- Submit drawings using an interactive canvas
- Mint NFTs for high-scoring drawings
- Track user statistics

## Technologies Used

- **Backend**: Node.js, Express
- **AI Image Generation**: Stability AI
- **IPFS Storage**: Pinata
- **Blockchain**: MultiversX (Devnet)
- **Warp Protocol**: For blockchain integration
- **Drawing Canvas**: Custom HTML5 Canvas implementation

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- MultiversX wallet (for blockchain interactions)
- Stability AI API key
- Pinata API key and secret

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file based on `.env.example` and fill in your API keys:
   ```
   STABILITY_API_KEY=your_stability_api_key
   PINATA_API_KEY=your_pinata_api_key
   PINATA_API_SECRET=your_pinata_api_secret
   WALLET_KEYSTORE_PATH=path_to_your_keystore_file
   WALLET_PASSWORD=your_wallet_password
   ```

### Running the Server

Start the server:
```
node server.js
```

The server will be available at http://localhost:3000.

### Testing the API

You can test the API endpoints directly from the web interface at http://localhost:3000.

The following endpoints are available:

- `POST /api/challenge/create`: Create a new drawing challenge
- `POST /api/drawing/submit`: Submit a drawing for scoring
- `POST /api/nft/mint`: Mint an NFT for a high-scoring drawing
- `GET /api/user/stats/:userAddress`: Get statistics for a user

### Warp Integration

The project is integrated with the MultiversX Warp Protocol. You can access the Warp at:

https://devnet.usewarp.to/drawdash

> **Note:** The Warp is currently configured to use `localhost:3000` URLs, which means it will only work when accessed from the same machine where the server is running. To make it accessible from other machines, you would need to deploy the server to a public URL and update the Warp actions accordingly.

The Warp provides the following actions:

- **Create Challenge**: Create a new drawing challenge with an AI-generated image
- **Submit Drawing**: Submit a drawing for a challenge and get a score
- **Mint NFT**: Mint an NFT for a high-scoring drawing
- **Get User Stats**: Get statistics for a user

### Drawing Canvas

The project includes a custom drawing canvas component that can be used to create drawings for challenges. You can test the drawing canvas at:

http://localhost:3000/frontend/index.html

Or use the dedicated route:

http://localhost:3000/drawing-canvas

The drawing canvas features:

- Color picker
- Brush size slider
- Undo/Redo functionality
- Clear canvas button
- Save drawing button

## Deployment

To deploy the Warp to the MultiversX devnet:

```
node scripts/deployWarp.js
```

This will create and register the Warp with the alias 'drawdash'.

### Using ngrok for Public Access

To make your localhost server accessible from the internet (useful for testing the Warp from different machines), you can use ngrok:

1. Install ngrok: https://ngrok.com/download
2. Start your server: `node server.js`
3. In a new terminal, run: `ngrok http 3000`
4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Update the Warp actions using the provided script:
   ```
   node scripts/updateWarpUrl.js https://abc123.ngrok.io
   ```
6. Redeploy the Warp: `node scripts/deployWarp.js`

Now your Warp will be accessible from any machine.

## Project Structure

- `server.js`: Main server file
- `warps/`: Warp-related files
  - `config.js`: Configuration for the Warp
  - `warpExecutor.js`: Handles Warp requests
  - `warpInfo.json`: Information about the deployed Warp
- `scripts/`: Utility scripts
  - `deployWarp.js`: Script to deploy the Warp
  - `testWarp.js`: Script to test the Warp
- `public/`: Static files
  - `index.html`: Web interface for testing the API
- `frontend/`: Frontend code
  - `DrawingCanvas.js`: Custom drawing canvas component
  - `index.html`: Demo page for the drawing canvas
- `temp/`: Temporary files
- `contracts/`: Smart contracts (to be implemented)

## Future Improvements

- Implement smart contracts for challenges and NFTs
- Develop a full frontend for the game
- Add user authentication
- Implement a leaderboard
- Add more game modes
- Improve the drawing canvas with more features
- Add real-time collaboration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [MultiversX](https://multiversx.com/)
- [Warp Protocol](https://usewarp.to/)
- [Stability AI](https://stability.ai/)
- [Pinata](https://pinata.cloud/) 