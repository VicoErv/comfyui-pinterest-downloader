import os
import folder_paths
from .pinterest_downloader import PinterestDownloader
from PIL import Image
import io

# Try to import ComfyUI progress utilities
try:
    import comfy.utils
    COMFY_PROGRESS_AVAILABLE = True
except ImportError:
    COMFY_PROGRESS_AVAILABLE = False


class PinterestDownloaderNode:
    """
    ComfyUI node for downloading images from Pinterest boards.
    Shows progress with image preview on the node.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pinterest_url": ("STRING", {
                    "multiline": False,
                    "default": "https://www.pinterest.com/username/board-name/"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("download_path",)
    FUNCTION = "download_pinterest"
    CATEGORY = "image/download"
    OUTPUT_NODE = True

    def download_pinterest(self, pinterest_url):
        """
        Download images from Pinterest board and return the absolute path.
        Shows progress with image preview in ComfyUI UI.

        Args:
            pinterest_url: URL of the Pinterest board

        Returns:
            tuple: (download_path,)
        """
        try:
            # Create unique directory for this download
            import uuid
            import time

            job_id = f"pinterest_{int(time.time())}_{str(uuid.uuid4())[:8]}"
            download_dir = os.path.join(self.output_dir, "pinterest", job_id)

            # Initialize downloader
            downloader = PinterestDownloader(download_dir)

            # Initialize progress bar if available
            pbar = None
            if COMFY_PROGRESS_AVAILABLE:
                pbar = comfy.utils.ProgressBar(100)  # Will update with actual total

            # Track last downloaded file path
            last_file_path = None

            # Progress tracking
            def progress_callback(current, total, filename):
                nonlocal last_file_path
                progress_percent = (current / total * 100) if total > 0 else 0

                # Store the file path for preview
                last_file_path = os.path.join(download_dir, filename)

                # Update ComfyUI progress bar with image preview
                if pbar is not None:
                    preview_bytes = None

                    # Try to load and convert the downloaded image to preview
                    if os.path.exists(last_file_path):
                        try:
                            img = Image.open(last_file_path)
                            # Resize for preview (max 512x512)
                            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
                            # Convert to JPEG bytes
                            buffer = io.BytesIO()
                            img.convert('RGB').save(buffer, format='JPEG', quality=85)
                            preview_bytes = buffer.getvalue()
                        except Exception as e:
                            print(f"[Pinterest] Could not generate preview: {e}")

                    pbar.update_absolute(current, total, preview_bytes)

                # Log to console
                print(f"[Pinterest] {current}/{total} ({progress_percent:.1f}%) - {filename}")

                return True  # Continue downloading

            # Download images
            print(f"[Pinterest Downloader] Starting download from: {pinterest_url}")
            file_count, total_size, final_path = downloader.download_board(
                pinterest_url,
                progress_callback
            )

            print(f"[Pinterest Downloader] Completed: {file_count} files downloaded")
            print(f"[Pinterest Downloader] Total size: {total_size / (1024*1024):.2f} MB")
            print(f"[Pinterest Downloader] Path: {final_path}")

            # Return absolute path
            abs_path = os.path.abspath(final_path)
            return (abs_path,)

        except Exception as e:
            error_msg = f"[Pinterest Downloader] Error: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "PinterestDownloader": PinterestDownloaderNode
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "PinterestDownloader": "Pinterest Downloader"
}
