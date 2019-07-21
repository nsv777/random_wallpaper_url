# import pprint
import re

import requests
from bs4 import BeautifulSoup

alphacoders_url = "https://wall.alphacoders.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def _get_big_url(url):
    soup = BeautifulSoup(requests.get(url + "random.php", headers=headers).text, features="lxml")

    return soup.find("a", {"href": re.compile('big\.php\?i=\d+')})["href"]


def get_wallpaper_url(url):
    soup = BeautifulSoup(requests.get(url + _get_big_url(url), headers=headers).text, features="lxml")

    return soup.find("div", {"class": "center img-container-desktop"}).find("a")["href"]


if __name__ == "__main__":
    # pp = pprint.PrettyPrinter()
    print(get_wallpaper_url(alphacoders_url))
