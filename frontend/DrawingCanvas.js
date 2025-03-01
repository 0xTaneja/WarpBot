/**
 * DrawingCanvas.js
 * A simple drawing canvas component for the DrawDash game
 */

class DrawingCanvas {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      throw new Error(`Container with ID "${containerId}" not found`);
    }

    // Default options
    this.options = {
      width: options.width || 500,
      height: options.height || 500,
      lineWidth: options.lineWidth || 5,
      lineColor: options.lineColor || '#000000',
      backgroundColor: options.backgroundColor || '#ffffff',
      toolbarPosition: options.toolbarPosition || 'top',
      showToolbar: options.showToolbar !== undefined ? options.showToolbar : true,
      showClearButton: options.showClearButton !== undefined ? options.showClearButton : true,
      showColorPicker: options.showColorPicker !== undefined ? options.showColorPicker : true,
      showSizeSlider: options.showSizeSlider !== undefined ? options.showSizeSlider : true,
      showUndoButton: options.showUndoButton !== undefined ? options.showUndoButton : true,
      showRedoButton: options.showRedoButton !== undefined ? options.showRedoButton : true,
      showSaveButton: options.showSaveButton !== undefined ? options.showSaveButton : true,
      onSave: options.onSave || null,
      onClear: options.onClear || null,
      onDraw: options.onDraw || null,
    };

    // Drawing state
    this.isDrawing = false;
    this.lastX = 0;
    this.lastY = 0;
    this.history = [];
    this.redoStack = [];
    this.currentHistoryStep = -1;

    // Create the canvas element
    this.createCanvas();

    // Create the toolbar if enabled
    if (this.options.showToolbar) {
      this.createToolbar();
    }

    // Initialize the canvas
    this.initCanvas();
  }

  /**
   * Create the canvas element and append it to the container
   */
  createCanvas() {
    // Create the canvas wrapper
    this.canvasWrapper = document.createElement('div');
    this.canvasWrapper.className = 'drawing-canvas-wrapper';
    this.canvasWrapper.style.position = 'relative';
    this.canvasWrapper.style.width = `${this.options.width}px`;
    this.canvasWrapper.style.height = `${this.options.height}px`;
    this.canvasWrapper.style.border = '1px solid #ccc';
    this.canvasWrapper.style.overflow = 'hidden';
    this.canvasWrapper.style.borderRadius = '4px';
    this.canvasWrapper.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';

    // Create the canvas element
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.options.width;
    this.canvas.height = this.options.height;
    this.canvas.style.position = 'absolute';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.backgroundColor = this.options.backgroundColor;
    this.canvas.style.cursor = 'crosshair';

    // Append the canvas to the wrapper
    this.canvasWrapper.appendChild(this.canvas);

    // Append the wrapper to the container
    this.container.appendChild(this.canvasWrapper);

    // Get the canvas context
    this.ctx = this.canvas.getContext('2d');
  }

  /**
   * Create the toolbar with drawing tools
   */
  createToolbar() {
    // Create the toolbar container
    this.toolbar = document.createElement('div');
    this.toolbar.className = 'drawing-canvas-toolbar';
    this.toolbar.style.display = 'flex';
    this.toolbar.style.alignItems = 'center';
    this.toolbar.style.justifyContent = 'space-between';
    this.toolbar.style.padding = '10px';
    this.toolbar.style.backgroundColor = '#f5f5f5';
    this.toolbar.style.borderRadius = '4px';
    this.toolbar.style.marginBottom = this.options.toolbarPosition === 'top' ? '10px' : '0';
    this.toolbar.style.marginTop = this.options.toolbarPosition === 'bottom' ? '10px' : '0';

    // Create the toolbar items container
    const toolbarItems = document.createElement('div');
    toolbarItems.style.display = 'flex';
    toolbarItems.style.alignItems = 'center';
    toolbarItems.style.gap = '10px';

    // Add color picker if enabled
    if (this.options.showColorPicker) {
      const colorPicker = document.createElement('input');
      colorPicker.type = 'color';
      colorPicker.value = this.options.lineColor;
      colorPicker.style.width = '30px';
      colorPicker.style.height = '30px';
      colorPicker.style.padding = '0';
      colorPicker.style.border = 'none';
      colorPicker.style.cursor = 'pointer';
      colorPicker.title = 'Choose color';
      colorPicker.addEventListener('input', (e) => {
        this.options.lineColor = e.target.value;
      });
      toolbarItems.appendChild(colorPicker);
    }

    // Add size slider if enabled
    if (this.options.showSizeSlider) {
      const sizeContainer = document.createElement('div');
      sizeContainer.style.display = 'flex';
      sizeContainer.style.alignItems = 'center';
      sizeContainer.style.gap = '5px';

      const sizeLabel = document.createElement('span');
      sizeLabel.textContent = 'Size:';
      sizeLabel.style.fontSize = '14px';
      sizeContainer.appendChild(sizeLabel);

      const sizeSlider = document.createElement('input');
      sizeSlider.type = 'range';
      sizeSlider.min = '1';
      sizeSlider.max = '50';
      sizeSlider.value = this.options.lineWidth;
      sizeSlider.style.width = '100px';
      sizeSlider.title = 'Brush size';
      sizeSlider.addEventListener('input', (e) => {
        this.options.lineWidth = parseInt(e.target.value, 10);
      });
      sizeContainer.appendChild(sizeSlider);

      toolbarItems.appendChild(sizeContainer);
    }

    // Add the toolbar items to the toolbar
    this.toolbar.appendChild(toolbarItems);

    // Create the toolbar buttons container
    const toolbarButtons = document.createElement('div');
    toolbarButtons.style.display = 'flex';
    toolbarButtons.style.alignItems = 'center';
    toolbarButtons.style.gap = '10px';

    // Add undo button if enabled
    if (this.options.showUndoButton) {
      const undoButton = this.createButton('Undo', () => this.undo());
      undoButton.title = 'Undo';
      toolbarButtons.appendChild(undoButton);
    }

    // Add redo button if enabled
    if (this.options.showRedoButton) {
      const redoButton = this.createButton('Redo', () => this.redo());
      redoButton.title = 'Redo';
      toolbarButtons.appendChild(redoButton);
    }

    // Add clear button if enabled
    if (this.options.showClearButton) {
      const clearButton = this.createButton('Clear', () => this.clear());
      clearButton.title = 'Clear canvas';
      toolbarButtons.appendChild(clearButton);
    }

    // Add save button if enabled
    if (this.options.showSaveButton) {
      const saveButton = this.createButton('Save', () => this.save());
      saveButton.title = 'Save drawing';
      toolbarButtons.appendChild(saveButton);
    }

    // Add the toolbar buttons to the toolbar
    this.toolbar.appendChild(toolbarButtons);

    // Append the toolbar to the container
    if (this.options.toolbarPosition === 'top') {
      this.container.insertBefore(this.toolbar, this.canvasWrapper);
    } else {
      this.container.appendChild(this.toolbar);
    }
  }

  /**
   * Create a button element with the given text and click handler
   * @param {string} text - The button text
   * @param {Function} onClick - The click handler
   * @returns {HTMLButtonElement} The button element
   */
  createButton(text, onClick) {
    const button = document.createElement('button');
    button.textContent = text;
    button.style.padding = '5px 10px';
    button.style.backgroundColor = '#4CAF50';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '4px';
    button.style.cursor = 'pointer';
    button.style.fontSize = '14px';
    button.addEventListener('click', onClick);
    return button;
  }

  /**
   * Initialize the canvas with event listeners
   */
  initCanvas() {
    // Set initial canvas state
    this.ctx.lineJoin = 'round';
    this.ctx.lineCap = 'round';
    this.ctx.lineWidth = this.options.lineWidth;
    this.ctx.strokeStyle = this.options.lineColor;

    // Fill the canvas with the background color
    this.ctx.fillStyle = this.options.backgroundColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Save the initial state to history
    this.saveToHistory();

    // Add event listeners for drawing
    this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
    this.canvas.addEventListener('mousemove', this.draw.bind(this));
    this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
    this.canvas.addEventListener('mouseout', this.stopDrawing.bind(this));

    // Add touch event listeners for mobile devices
    this.canvas.addEventListener('touchstart', this.handleTouchStart.bind(this));
    this.canvas.addEventListener('touchmove', this.handleTouchMove.bind(this));
    this.canvas.addEventListener('touchend', this.handleTouchEnd.bind(this));
  }

  /**
   * Handle touch start event
   * @param {TouchEvent} e - The touch event
   */
  handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const mouseEvent = new MouseEvent('mousedown', {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    this.canvas.dispatchEvent(mouseEvent);
  }

  /**
   * Handle touch move event
   * @param {TouchEvent} e - The touch event
   */
  handleTouchMove(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const mouseEvent = new MouseEvent('mousemove', {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    this.canvas.dispatchEvent(mouseEvent);
  }

  /**
   * Handle touch end event
   * @param {TouchEvent} e - The touch event
   */
  handleTouchEnd(e) {
    e.preventDefault();
    const mouseEvent = new MouseEvent('mouseup', {});
    this.canvas.dispatchEvent(mouseEvent);
  }

  /**
   * Start drawing on the canvas
   * @param {MouseEvent} e - The mouse event
   */
  startDrawing(e) {
    const rect = this.canvas.getBoundingClientRect();
    this.lastX = e.clientX - rect.left;
    this.lastY = e.clientY - rect.top;
    this.isDrawing = true;

    // Start a new path
    this.ctx.beginPath();
    this.ctx.moveTo(this.lastX, this.lastY);
    this.ctx.lineTo(this.lastX, this.lastY);
    this.ctx.stroke();
  }

  /**
   * Draw on the canvas
   * @param {MouseEvent} e - The mouse event
   */
  draw(e) {
    if (!this.isDrawing) return;

    const rect = this.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Set the line properties
    this.ctx.lineWidth = this.options.lineWidth;
    this.ctx.strokeStyle = this.options.lineColor;

    // Draw the line
    this.ctx.beginPath();
    this.ctx.moveTo(this.lastX, this.lastY);
    this.ctx.lineTo(x, y);
    this.ctx.stroke();

    // Update the last position
    this.lastX = x;
    this.lastY = y;

    // Call the onDraw callback if provided
    if (this.options.onDraw) {
      this.options.onDraw();
    }
  }

  /**
   * Stop drawing on the canvas
   */
  stopDrawing() {
    if (this.isDrawing) {
      this.isDrawing = false;
      this.saveToHistory();
    }
  }

  /**
   * Save the current canvas state to history
   */
  saveToHistory() {
    // Remove any future states if we're in the middle of the history
    if (this.currentHistoryStep < this.history.length - 1) {
      this.history = this.history.slice(0, this.currentHistoryStep + 1);
      this.redoStack = [];
    }

    // Save the current state
    this.history.push(this.canvas.toDataURL());
    this.currentHistoryStep = this.history.length - 1;
  }

  /**
   * Undo the last drawing action
   */
  undo() {
    if (this.currentHistoryStep > 0) {
      this.redoStack.push(this.history[this.currentHistoryStep]);
      this.currentHistoryStep--;
      this.loadFromHistory();
    }
  }

  /**
   * Redo the last undone drawing action
   */
  redo() {
    if (this.redoStack.length > 0) {
      this.currentHistoryStep++;
      this.history[this.currentHistoryStep] = this.redoStack.pop();
      this.loadFromHistory();
    }
  }

  /**
   * Load the current history step onto the canvas
   */
  loadFromHistory() {
    const img = new Image();
    img.src = this.history[this.currentHistoryStep];
    img.onload = () => {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.drawImage(img, 0, 0);
    };
  }

  /**
   * Clear the canvas
   */
  clear() {
    this.ctx.fillStyle = this.options.backgroundColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.saveToHistory();

    // Call the onClear callback if provided
    if (this.options.onClear) {
      this.options.onClear();
    }
  }

  /**
   * Save the drawing as a base64 encoded PNG
   * @returns {string} The base64 encoded PNG
   */
  save() {
    const dataURL = this.canvas.toDataURL('image/png');
    
    // Call the onSave callback if provided
    if (this.options.onSave) {
      this.options.onSave(dataURL);
    }
    
    return dataURL;
  }

  /**
   * Get the drawing as a base64 encoded PNG
   * @returns {string} The base64 encoded PNG
   */
  getDrawingData() {
    return this.canvas.toDataURL('image/png');
  }

  /**
   * Load an image onto the canvas
   * @param {string} src - The image source (URL or base64)
   * @param {Function} callback - The callback function to call when the image is loaded
   */
  loadImage(src, callback) {
    const img = new Image();
    img.src = src;
    img.onload = () => {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
      this.saveToHistory();
      if (callback) {
        callback();
      }
    };
  }

  /**
   * Resize the canvas
   * @param {number} width - The new width
   * @param {number} height - The new height
   */
  resize(width, height) {
    // Save the current drawing
    const currentDrawing = this.canvas.toDataURL();

    // Update the canvas size
    this.canvas.width = width;
    this.canvas.height = height;
    this.canvasWrapper.style.width = `${width}px`;
    this.canvasWrapper.style.height = `${height}px`;

    // Restore the drawing
    this.loadImage(currentDrawing);
  }
}

// Export the DrawingCanvas class
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DrawingCanvas;
} 