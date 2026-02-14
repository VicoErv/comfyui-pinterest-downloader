#!/bin/bash
# Installation script for ComfyUI Pinterest Downloader Node

echo "ComfyUI Pinterest Downloader - Installation Script"
echo "=================================================="
echo ""

# Check if ComfyUI path is provided
if [ -z "$1" ]; then
    echo "Usage: ./install.sh /path/to/ComfyUI"
    echo ""
    echo "Example: ./install.sh ~/ComfyUI"
    echo ""
    exit 1
fi

COMFYUI_PATH="$1"
CUSTOM_NODES_PATH="$COMFYUI_PATH/custom_nodes"
TARGET_PATH="$CUSTOM_NODES_PATH/comfyui-pinterest-downloader"

# Check if ComfyUI directory exists
if [ ! -d "$COMFYUI_PATH" ]; then
    echo "Error: ComfyUI directory not found at: $COMFYUI_PATH"
    exit 1
fi

# Check if custom_nodes directory exists
if [ ! -d "$CUSTOM_NODES_PATH" ]; then
    echo "Error: custom_nodes directory not found at: $CUSTOM_NODES_PATH"
    exit 1
fi

echo "ComfyUI Path: $COMFYUI_PATH"
echo "Target Path: $TARGET_PATH"
echo ""

# Copy files
echo "Copying files..."
if [ -d "$TARGET_PATH" ]; then
    echo "Warning: Directory already exists. Removing old version..."
    rm -rf "$TARGET_PATH"
fi

mkdir -p "$TARGET_PATH"
cp -r ./* "$TARGET_PATH/"

echo "✓ Files copied successfully"
echo ""

# Install dependencies
echo "Installing dependencies..."
cd "$TARGET_PATH"

if command -v pip &> /dev/null; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "Warning: pip not found. Please install dependencies manually:"
    echo "  pip install -r $TARGET_PATH/requirements.txt"
fi

echo ""
echo "=================================================="
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart ComfyUI"
echo "2. Look for 'Pinterest Downloader' node in the 'image/download' category"
echo "3. Add it to your workflow and enter a Pinterest board URL"
echo ""
echo "For testing, you can run:"
echo "  cd $TARGET_PATH"
echo "  python test_downloader.py https://www.pinterest.com/username/board/"
echo ""
