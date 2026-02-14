import subprocess
import os
import json
import tempfile


class PinterestDownloader:
    """
    Pinterest downloader using gallery-dl for proper pagination support.
    Downloads ALL pins from a board, not just the initial page.
    """

    def __init__(self, download_dir: str):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def download_board(self, url: str) -> tuple[int, int, str]:
        """
        Download all images from a Pinterest board using gallery-dl.

        Args:
            url: Pinterest board URL

        Returns:
            tuple: (successful_downloads, total_size_bytes, download_dir)
        """
        import shutil

        # Check if gallery-dl is installed
        if not shutil.which("gallery-dl"):
            raise Exception("gallery-dl is not installed. Run: pip install gallery-dl")

        # Create temporary config file for gallery-dl
        config = {
            "extractor": {
                "pinterest": {
                    "directory": [self.download_dir],
                    "filename": "{id}.{extension}"
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_path = f.name

        try:
            print(f"[Pinterest] Starting download from: {url}")
            print(f"[Pinterest] Download directory: {self.download_dir}")

            # Run gallery-dl silently
            result = subprocess.run(
                ["gallery-dl", url, "-c", config_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception(f"gallery-dl exited with code {result.returncode}")

            # Count downloaded files
            file_count = 0
            total_size = 0

            if os.path.exists(self.download_dir):
                for root, dirs, files in os.walk(self.download_dir):
                    for file in files:
                        if not file.startswith('.'):
                            file_count += 1
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)

            print(f"[Pinterest] Download complete: {file_count} files, {total_size / (1024*1024):.2f} MB")
            return file_count, total_size, self.download_dir

        finally:
            # Clean up config file
            if os.path.exists(config_path):
                os.remove(config_path)
