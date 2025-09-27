import re
from typing import Optional
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class WallpaperError(Exception):
    """Custom exception for wallpaper fetching errors."""
    pass


class Wallpaper(object):
    BASE_URL = "https://wall.alphacoders.com"
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    BROWSER_CONFIG = {
        'browser': 'firefox',
        'platform': 'linux',
        'desktop': True
    }

    def __init__(self, delay: int = 10):
        self.scraper = cloudscraper.create_scraper(delay=delay, browser=self.BROWSER_CONFIG)

    def _get_big_url_path(self) -> str:
        """Fetches the relative path to the wallpaper's detail page."""
        random_page_url = urljoin(self.BASE_URL, "random.php")
        try:
            response = self.scraper.get(random_page_url, headers=self.HEADERS)
            response.raise_for_status()
        except RequestException as e:
            raise WallpaperError(f"Failed to fetch random page: {e}") from e

        soup = BeautifulSoup(response.text, features="lxml")
        link_tag = soup.find("a", {"href": re.compile(r'big\.php\?i=\d+')})

        if not link_tag:
            raise WallpaperError("Could not find the 'big.php' link on the random page.")

        return link_tag["href"]

    def get_wallpaper_url(self) -> Optional[str]:
        """Fetches and returns the direct URL to a random wallpaper image."""
        big_url_path = self._get_big_url_path()
        full_big_url = urljoin(self.BASE_URL, big_url_path)

        try:
            response = self.scraper.get(full_big_url, headers=self.HEADERS)
            response.raise_for_status()
        except RequestException as e:
            raise WallpaperError(f"Failed to fetch wallpaper details page: {e}") from e

        soup = BeautifulSoup(response.text, features="lxml")
        img_tag = soup.find("img", {"id": "main-content"})

        if not img_tag or not img_tag.get("src"):
            raise WallpaperError("Could not find the main image source URL.")

        return img_tag["src"]


if __name__ == "__main__":
    wallpaper = Wallpaper()
    image_url = wallpaper.get_wallpaper_url()
    print(image_url)
