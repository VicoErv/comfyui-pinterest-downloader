#!/usr/bin/env python3
"""
Test script for Pinterest Downloader
Run this to test the downloader before integrating with ComfyUI
"""

import os
import sys
from pinterest_downloader import PinterestDownloader


def test_download(url, output_dir="./test_downloads"):
    """
    Test the Pinterest downloader with a given URL.

    Args:
        url: Pinterest board URL
        output_dir: Directory to save test downloads
    """
    print(f"Testing Pinterest Downloader")
    print(f"URL: {url}")
    print(f"Output: {output_dir}")
    print("-" * 60)

    try:
        # Create downloader
        downloader = PinterestDownloader(output_dir)

        # Progress callback
        def progress(current, total, filename):
            percent = (current / total * 100) if total > 0 else 0
            print(f"Progress: {current}/{total} ({percent:.1f}%) - {filename}")
            return True

        # Download
        print("\nStarting download...")
        file_count, total_size, path = downloader.download_board(url, progress)

        # Results
        print("\n" + "=" * 60)
        print(f"✓ Download completed successfully!")
        print(f"Files downloaded: {file_count}")
        print(f"Total size: {total_size / (1024*1024):.2f} MB")
        print(f"Absolute path: {os.path.abspath(path)}")
        print("=" * 60)

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Error: {str(e)}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    # Example URL - replace with your own
    test_url = "https://www.pinterest.com/username/board-name/"

    # Check if URL provided as argument
    if len(sys.argv) > 1:
        test_url = sys.argv[1]

    print("Pinterest Downloader Test Script")
    print("=" * 60)
    print(f"Usage: python test_downloader.py [pinterest_url]")
    print(f"Current URL: {test_url}")
    print()

    # Run test
    success = test_download(test_url)

    sys.exit(0 if success else 1)
