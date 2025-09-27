import unittest
from unittest.mock import patch, Mock, call
from urllib.parse import urljoin

from requests.exceptions import RequestException

from random_wallpaper_url import Wallpaper, WallpaperError


class TestWallpaper(unittest.TestCase):

    @patch('random_wallpaper_url.cloudscraper.create_scraper')
    def setUp(self, mock_create_scraper):
        """Set up a test client and mock scraper for each test."""
        # We mock the scraper to avoid real network calls
        self.mock_scraper = Mock()
        # Mock the response object that scraper.get() would return
        self.mock_response = Mock()
        self.mock_scraper.get.return_value = self.mock_response
        mock_create_scraper.return_value = self.mock_scraper
        self.wallpaper = Wallpaper()

    def test_get_big_url_path_success(self):
        """
        Test that _get_big_url_path correctly parses the 'big.php' link on success.
        """
        # Sample HTML that would be returned from the /random.php page
        mock_html_random = """
        <html>
            <body>
                <a href="big.php?i=123456">
                    <img src="thumb-123456.jpg" />
                </a>
            </body>
        </html>
        """
        # Configure the mock scraper to return our sample HTML
        self.mock_response.text = mock_html_random

        # Call the method we are testing
        big_url_path = self.wallpaper._get_big_url_path()

        # Assert that the correct URL was extracted
        self.assertEqual(big_url_path, "big.php?i=123456")
        # Verify that the scraper's get method was called correctly
        self.mock_scraper.get.assert_called_once_with(
            urljoin(self.wallpaper.BASE_URL, "random.php"),
            headers=self.wallpaper.HEADERS
        )
        # Verify that we checked the status code of the response
        self.mock_response.raise_for_status.assert_called_once()

    def test_get_big_url_path_raises_error_on_network_failure(self):
        """Test that _get_big_url_path raises WallpaperError on network failure."""
        self.mock_scraper.get.side_effect = RequestException("Connection timed out")

        with self.assertRaisesRegex(WallpaperError, "Failed to fetch random page"):
            self.wallpaper._get_big_url_path()

    def test_get_big_url_path_raises_error_on_missing_link(self):
        """Test that _get_big_url_path raises WallpaperError if the link is not found."""
        self.mock_response.text = "<html><body>No link here!</body></html>"

        with self.assertRaisesRegex(WallpaperError, "Could not find the 'big.php' link"):
            self.wallpaper._get_big_url_path()

    def test_get_wallpaper_url_success(self):
        """
        Test that get_wallpaper_url correctly extracts the final image source URL on success.
        """
        # Sample HTML for the two pages the method fetches
        mock_html_random = '<html><body><a href="big.php?i=78910">Link</a></body></html>'
        mock_html_big = """
        <html>
            <body>
                <picture>
                    <img id="main-content" src="https://images.alphacoders.com/789/78910.jpg" />
                </picture>
            </body>
        </html>
        """

        # Configure the mock scraper to return different HTML for each call
        mock_response_random = Mock()
        mock_response_random.raise_for_status.return_value = None
        mock_response_random.text = mock_html_random

        mock_response_big = Mock()
        mock_response_big.raise_for_status.return_value = None
        mock_response_big.text = mock_html_big

        self.mock_scraper.get.side_effect = [mock_response_random, mock_response_big]

        # Call the method we are testing
        wallpaper_url = self.wallpaper.get_wallpaper_url()

        # Assert that the final wallpaper URL is correct
        self.assertEqual(wallpaper_url, "https://images.alphacoders.com/789/78910.jpg")

        # Verify the correct sequence of network calls
        expected_calls = [
            call(
                urljoin(self.wallpaper.BASE_URL, "random.php"),
                headers=self.wallpaper.HEADERS
            ),
            call(
                urljoin(self.wallpaper.BASE_URL, "big.php?i=78910"),
                headers=self.wallpaper.HEADERS
            )
        ]
        self.mock_scraper.get.assert_has_calls(expected_calls)
        self.assertEqual(self.mock_scraper.get.call_count, 2)

    def test_get_wallpaper_url_raises_error_on_missing_image(self):
        """Test get_wallpaper_url raises WallpaperError if the final image tag is missing."""
        mock_html_random = '<html><body><a href="big.php?i=78910">Link</a></body></html>'
        mock_html_big_no_image = "<html><body><p>Image not found</p></body></html>"

        mock_response_random = Mock(text=mock_html_random)
        mock_response_big = Mock(text=mock_html_big_no_image)
        self.mock_scraper.get.side_effect = [mock_response_random, mock_response_big]

        with self.assertRaisesRegex(WallpaperError, "Could not find the main image source URL"):
            self.wallpaper.get_wallpaper_url()


if __name__ == '__main__':
    unittest.main()