const warpActions = require('./warpActions');

/**
 * Execute a Warp action with the given parameters
 * @param {string} actionName - The name of the action to execute
 * @param {Object} args - The arguments for the action
 * @returns {Promise<Object>} - The result of the action
 */
async function executeWarpAction(actionName, args = {}) {
  try {
    console.log(`Executing Warp action: ${actionName}`);
    console.log(`Arguments:`, args);
    
    // Check if the action exists
    if (!warpActions[actionName]) {
      throw new Error(`Action '${actionName}' not found`);
    }
    
    // Execute the action
    const result = await warpActions[actionName](args);
    
    console.log(`Action '${actionName}' executed successfully`);
    console.log(`Result:`, result);
    
    return result;
  } catch (error) {
    console.error(`Error executing Warp action '${actionName}':`, error);
    return {
      status: 'error',
      message: `Failed to execute action '${actionName}': ${error.message}`
    };
  }
}

/**
 * Handle a Warp request
 * @param {Object} request - The Warp request object
 * @returns {Promise<Object>} - The response to the Warp request
 */
async function handleWarpRequest(request) {
  try {
    console.log('Handling Warp request:', request);
    
    // Extract the action and arguments from the request
    const { action, args } = request;
    
    if (!action) {
      throw new Error('No action specified in the request');
    }
    
    // Execute the action
    const result = await executeWarpAction(action, args || {});
    
    return {
      success: result.status === 'success',
      message: result.message,
      data: result.data
    };
  } catch (error) {
    console.error('Error handling Warp request:', error);
    return {
      success: false,
      message: `Failed to handle Warp request: ${error.message}`,
      data: null
    };
  }
}

module.exports = {
  executeWarpAction,
  handleWarpRequest
}; 