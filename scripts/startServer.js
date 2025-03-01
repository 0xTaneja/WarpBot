const { spawn } = require('child_process');
const path = require('path');

// Start the server
function startServer() {
  console.log('Starting DrawDash server...');
  
  const serverPath = path.resolve(__dirname, '..', 'server.js');
  
  // Spawn the server process
  const serverProcess = spawn('node', [serverPath], {
    stdio: 'inherit',
    detached: false
  });
  
  // Handle server process events
  serverProcess.on('error', (error) => {
    console.error('Failed to start server:', error);
  });
  
  serverProcess.on('exit', (code, signal) => {
    if (code !== 0) {
      console.error(`Server process exited with code ${code} and signal ${signal}`);
    } else {
      console.log('Server process exited normally');
    }
  });
  
  // Return the server process
  return serverProcess;
}

// Run the server if this script is executed directly
if (require.main === module) {
  const serverProcess = startServer();
  
  // Handle process termination
  process.on('SIGINT', () => {
    console.log('Received SIGINT. Shutting down server...');
    if (serverProcess) {
      serverProcess.kill('SIGINT');
    }
    process.exit(0);
  });
  
  process.on('SIGTERM', () => {
    console.log('Received SIGTERM. Shutting down server...');
    if (serverProcess) {
      serverProcess.kill('SIGTERM');
    }
    process.exit(0);
  });
}

module.exports = {
  startServer
}; 