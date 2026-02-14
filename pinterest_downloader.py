import requests
import os
import re
import json
from urllib.parse import urlparse
from typing import List, Callable, Optional
import time


class PinterestDownloader:
    """
    Native Pinterest downloader with progress tracking.
    """

    def __init__(self, download_dir: str):
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.pinterest.com/'
        })

    def extract_board_id(self, url: str) -> Optional[str]:
        """Extract board ID from Pinterest URL."""
        # Pattern: https://pinterest.com/username/board-name/
        match = re.search(r'pinterest\.com/([^/]+)/([^/]+)', url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return None

    def get_image_urls(self, url: str) -> List[str]:
        """
        Fetch all image URLs from a Pinterest board.
        Extracts structured data from Pinterest's embedded JSON.
        """
        image_urls = []

        try:
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            content = response.text

            # Pinterest embeds data in <script id="__PWS_DATA__"> tags
            # Look for the structured JSON data
            json_match = re.search(r'<script id="__PWS_DATA__" type="application/json">(.+?)</script>', content, re.DOTALL)

            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    # Navigate through the JSON structure to find pins
                    # Pinterest's structure: data -> props -> initialReduxState -> pins
                    if isinstance(data, dict):
                        # Try to find pins in the data structure
                        pins = self._extract_pins_from_data(data)
                        for pin in pins:
                            # Get the original image URL
                            if 'images' in pin and 'orig' in pin['images']:
                                img_url = pin['images']['orig']['url']
                                if img_url and img_url not in image_urls:
                                    image_urls.append(img_url)
                except json.JSONDecodeError:
                    pass

            # Fallback: if JSON parsing didn't work, use regex but be more selective
            if not image_urls:
                # Only look for originals, not thumbnails
                pattern = r'"url":\s*"(https://i\.pinimg\.com/originals/[^"]+\.(?:jpg|jpeg|png|gif))"'
                matches = re.findall(pattern, content)

                # Remove duplicates while preserving order
                seen = set()
                for match in matches:
                    if match not in seen:
                        seen.add(match)
                        image_urls.append(match)

        except Exception as e:
            raise

        return image_urls

    def _extract_pins_from_data(self, data: dict, pins: list = None) -> list:
        """
        Recursively extract pins from Pinterest's JSON data structure.
        """
        if pins is None:
            pins = []

        if isinstance(data, dict):
            # Check if this dict looks like a pin object
            if 'images' in data and 'id' in data:
                pins.append(data)
            # Recursively search nested structures
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._extract_pins_from_data(value, pins)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._extract_pins_from_data(item, pins)

        return pins

    def download_image(self, url: str, filepath: str) -> bool:
        """Download a single image."""
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True
        except Exception as e:
            return False

    def download_board(
        self,
        url: str,
        progress_callback: Optional[Callable[[int, int, str], bool]] = None
    ) -> tuple[int, int, str]:
        """
        Download all images from a Pinterest board.

        Args:
            url: Pinterest board URL
            progress_callback: Callback function(current, total, filename) -> bool
                              Returns False to cancel download

        Returns:
            tuple: (successful_downloads, total_size_bytes, download_dir)
        """
        # Create job-specific directory
        os.makedirs(self.download_dir, exist_ok=True)

        # Get all image URLs
        image_urls = self.get_image_urls(url)

        if not image_urls:
            raise Exception("No images found on this Pinterest board")

        # Download each image
        successful = 0
        total_size = 0

        for idx, img_url in enumerate(image_urls, 1):
            # Generate filename from URL
            filename = os.path.basename(urlparse(img_url).path)
            if not filename:
                filename = f"image_{idx}.jpg"

            filepath = os.path.join(self.download_dir, filename)

            # Check if file already exists and is valid
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                # File already exists, skip download
                successful += 1
                total_size += os.path.getsize(filepath)

                # Still call progress callback
                if progress_callback:
                    should_continue = progress_callback(idx, len(image_urls), filename)
                    if should_continue is False:
                        break

                continue

            # Call progress callback and check for cancellation
            if progress_callback:
                should_continue = progress_callback(idx, len(image_urls), filename)
                if should_continue is False:
                    # Cancellation requested
                    break

            # Download the image
            if self.download_image(img_url, filepath):
                successful += 1
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)

            # Small delay to avoid rate limiting
            time.sleep(0.5)

        return successful, total_size, self.download_dir
