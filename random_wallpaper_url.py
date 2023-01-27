# import pprint
import re

import cloudscraper
from bs4 import BeautifulSoup

alphacoders_url = "https://wall.alphacoders.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def _get_big_url(url, scraper):
    soup = BeautifulSoup(scraper.get(url + "random.php", headers=headers).text, features="lxml")

    return soup.find("a", {"href": re.compile('big\.php\?i=\d+')})["href"]


def get_wallpaper_url(url):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    soup = BeautifulSoup(scraper.get(url + _get_big_url(url=url, scraper=scraper), headers=headers).text, features="lxml")

    return soup.find("div", {"class": "center img-container-desktop"}).find("img")["src"]


if __name__ == "__main__":
    # pp = pprint.PrettyPrinter()
    print(get_wallpaper_url(url=alphacoders_url))

