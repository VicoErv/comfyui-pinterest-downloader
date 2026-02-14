# ComfyUI Pinterest Downloader Node

A custom node for ComfyUI that downloads images from Pinterest boards.

## Features

- Download all images from a Pinterest board
- **Real-time image preview on the node** - see each downloaded image displayed on the node
- Progress bar showing download progress (X/Y images)
- Progress also logged to console as fallback
- Returns absolute path to downloaded images
- Automatic organization in ComfyUI output directory
- Original quality images only

## Installation

1. Navigate to your ComfyUI custom_nodes directory:
```bash
cd ComfyUI/custom_nodes/
```

2. Clone or copy this directory:
```bash
git clone <repository-url> comfyui-pinterest-downloader
# OR
cp -r /path/to/comfyui-pinterest-downloader ./
```

3. Install dependencies:
```bash
cd comfyui-pinterest-downloader
pip install -r requirements.txt
```

4. Restart ComfyUI

## Usage

1. Add the "Pinterest Downloader" node to your workflow
2. Enter a Pinterest board URL (e.g., `https://www.pinterest.com/username/board-name/`)
3. Connect the output to other nodes that need the image directory path
4. Run the workflow

### Input

- **pinterest_url** (STRING): URL of the Pinterest board to download

### Output

- **download_path** (STRING): Absolute path to the directory containing downloaded images

## Example Workflow

```
Pinterest Downloader Node
    ↓ (download_path)
Load Images from Directory Node
    ↓
Your Image Processing Nodes
```

## Output Structure

Downloaded images are saved to:
```
ComfyUI/output/pinterest/pinterest_{timestamp}_{id}/
├── image_1.jpg
├── image_2.jpg
└── ...
```

## Progress Tracking

Progress is displayed **directly on the ComfyUI node** during execution:

**On the Node:**
- Progress bar showing current/total (e.g., "5/27")
- **Live image preview** - each downloaded image is displayed on the node as it's saved
- Preview updates automatically with each new download

**In Console:**
```
[Pinterest] 1/27 (3.7%) - image_1.jpg
[Pinterest] 2/27 (7.4%) - image_2.jpg
...
[Pinterest Downloader] Completed: 27 files downloaded
[Pinterest Downloader] Total size: 15.32 MB
[Pinterest Downloader] Path: /absolute/path/to/images
```

## Notes

- The node creates a unique directory for each download
- Images are downloaded with a 0.5s delay between requests to avoid rate limiting
- Only original quality images are downloaded (no thumbnails)
- Supports JPG, JPEG, PNG, and GIF formats

## Troubleshooting

**No images found:**
- Verify the Pinterest URL is correct and accessible
- Some private boards may not be accessible

**Download fails:**
- Check your internet connection
- Pinterest may be rate limiting - try again later
- Check ComfyUI console for detailed error messages

## Requirements

- Python 3.8+
- requests >= 2.32.0
- Pillow >= 10.0.0
- ComfyUI

## License

MIT
