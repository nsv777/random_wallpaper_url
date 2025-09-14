# import pprint
import re

import cloudscraper
import requests
from bs4 import BeautifulSoup

alphacoders_url = "https://wall.alphacoders.com"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
browser = {
    'browser': 'firefox',
    'platform': 'linux',
    'desktop': True
}


class Wallpaper(object):
    def __init__(self):
        self.session = requests.session()
        self.scraper = cloudscraper.create_scraper(delay=20, browser=browser, sess=self.session)

    def _get_big_url(self, url: str) -> str:
        scraper_text = self.scraper.get(f"{url}/random.php", headers=headers).text
        soup = BeautifulSoup(scraper_text, features="lxml")

        return soup.find("a", {"href": re.compile('big\\.php\\?i=\\d+')})["href"]

    def get_wallpaper_url(self, url: str) -> str:
        big_url = self._get_big_url(url=url)
        soup = BeautifulSoup(self.scraper.get(big_url, headers=headers).text, features="lxml")

        return soup.find("picture").find("img", {"id": "main-content"})["src"]


if __name__ == "__main__":
    # pp = pprint.PrettyPrinter()
    wallpaper = Wallpaper()
    print(wallpaper.get_wallpaper_url(url=alphacoders_url))
