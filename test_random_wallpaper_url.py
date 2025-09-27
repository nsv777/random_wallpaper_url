import unittest
from unittest.mock import patch, Mock

from random_wallpaper_url import Wallpaper, alphacoders_url


class TestWallpaper(unittest.TestCase):

    @patch('random_wallpaper_url.cloudscraper.create_scraper')
    def setUp(self, mock_create_scraper):
        """Set up a test client and mock scraper for each test."""
        # We mock the scraper to avoid real network calls
        self.mock_scraper = Mock()
        mock_create_scraper.return_value = self.mock_scraper
        self.wallpaper = Wallpaper()

    def test_get_big_url(self):
        """
        Test that _get_big_url correctly parses the 'big.php' link.
        """
        # Sample HTML that would be returned from the /random.php page
        mock_html_random = """
        <html>
            <body>
                <a href="big.php?i=123456">
                    <img src="thumb-123456.jpg">
                </a>
            </body>
        </html>
        """
        # Configure the mock scraper to return our sample HTML
        self.mock_scraper.get.return_value.text = mock_html_random

        # Call the method we are testing
        big_url = self.wallpaper._get_big_url(url=alphacoders_url)

        # Assert that the correct URL was extracted
        self.assertEqual(big_url, "big.php?i=123456")
        # Verify that the scraper's get method was called correctly
        self.mock_scraper.get.assert_called_once_with(
            f"{alphacoders_url}/random.php",
            headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

    def test_get_wallpaper_url(self):
        """
        Test that get_wallpaper_url correctly extracts the final image source URL.
        """
        # Sample HTML for the two pages the method fetches
        mock_html_random = '<html><body><a href="big.php?i=78910">Link</a></body></html>'
        mock_html_big = """
        <html>
            <body>
                <picture>
                    <img id="main-content" src="https://images.alphacoders.com/789/78910.jpg">
                </picture>
            </body>
        </html>
        """

        # Configure the mock scraper to return different HTML for each call
        mock_response_random = Mock()
        mock_response_random.text = mock_html_random

        mock_response_big = Mock()
        mock_response_big.text = mock_html_big

        self.mock_scraper.get.side_effect = [mock_response_random, mock_response_big]

        # Call the method we are testing
        wallpaper_url = self.wallpaper.get_wallpaper_url(url=alphacoders_url)

        # Assert that the final wallpaper URL is correct
        self.assertEqual(wallpaper_url, "https://images.alphacoders.com/789/78910.jpg")
        self.assertEqual(self.mock_scraper.get.call_count, 2)


if __name__ == '__main__':
    unittest.main()