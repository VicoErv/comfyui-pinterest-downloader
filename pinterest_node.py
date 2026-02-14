import os
import folder_paths
from .pinterest_downloader import PinterestDownloader


class PinterestDownloaderNode:
    """
    ComfyUI node for downloading images from Pinterest boards.
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

            # Download images
            file_count, total_size, final_path = downloader.download_board(pinterest_url)

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
