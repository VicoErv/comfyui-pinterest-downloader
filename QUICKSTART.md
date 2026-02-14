# Quick Start Guide

## Installation

### Option 1: Automatic Installation (Recommended)

```bash
cd /Users/vico/WebstormProjects/mlops/comfyui-pinterest-downloader
./install.sh /path/to/your/ComfyUI
```

### Option 2: Manual Installation

```bash
# Copy to ComfyUI custom_nodes
cp -r /Users/vico/WebstormProjects/mlops/comfyui-pinterest-downloader \
      /path/to/ComfyUI/custom_nodes/

# Install dependencies
cd /path/to/ComfyUI/custom_nodes/comfyui-pinterest-downloader
pip install -r requirements.txt
```

## Testing Before Installation

Test the downloader independently:

```bash
cd /Users/vico/WebstormProjects/mlops/comfyui-pinterest-downloader
python test_downloader.py "https://www.pinterest.com/username/board-name/"
```

## Using in ComfyUI

1. **Restart ComfyUI** after installation
2. **Find the node**: Search for "Pinterest Downloader" or look in `image/download` category
3. **Add to workflow**: Drag the node into your workflow
4. **Configure**: Enter a Pinterest board URL
5. **Connect output**: The `download_path` output provides the absolute path to downloaded images
6. **Run**: Execute the workflow and **watch live image previews on the node** as images download

### What You'll See

- **On the node**: Live preview of each downloaded image + progress bar (5/27)
- **In console**: Detailed progress with filenames and percentages

## Example Workflow

```
┌─────────────────────────┐
│ Pinterest Downloader    │
│ URL: pinterest.com/...  │
└───────────┬─────────────┘
            │ download_path
            ▼
┌─────────────────────────┐
│ Load Images from Dir    │
└───────────┬─────────────┘
            │ images
            ▼
┌─────────────────────────┐
│ Your Processing Nodes   │
└─────────────────────────┘
```

## Output Location

Images are saved to:
```
ComfyUI/output/pinterest/pinterest_{timestamp}_{id}/
```

Each download creates a unique directory with all images from the board.

## Console Output Example

Progress is shown **in the ComfyUI UI above the node** and also logged to console:

```
[Pinterest Downloader] Starting download from: https://...
[Pinterest] 1/27 (3.7%) - image_1.jpg
[Pinterest] 2/27 (7.4%) - image_2.jpg
...
[Pinterest] 27/27 (100.0%) - image_27.jpg
[Pinterest Downloader] Completed: 27 files downloaded
[Pinterest Downloader] Total size: 15.32 MB
[Pinterest Downloader] Path: /absolute/path/to/ComfyUI/output/pinterest/...
```

## Troubleshooting

**Node doesn't appear in ComfyUI:**
- Make sure you restarted ComfyUI after installation
- Check the console for any import errors
- Verify files are in the correct location: `ComfyUI/custom_nodes/comfyui-pinterest-downloader/`

**Download fails:**
- Test with `test_downloader.py` first
- Check the Pinterest URL is valid and accessible
- Verify internet connection
- Check console for detailed error messages

**No images found:**
- Some Pinterest boards may be private or restricted
- Try a different public board
- Verify the URL format is correct

## Project Location

Full path: `/Users/vico/WebstormProjects/mlops/comfyui-pinterest-downloader/`

## Support

For issues or questions, check the README.md file for detailed documentation.
