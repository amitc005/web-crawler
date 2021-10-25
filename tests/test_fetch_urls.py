import unittest
from unittest.mock import patch
from web_crawler import fetch_urls

URL = "https://test.com"


class TestFetchURls(unittest.TestCase):
    @patch("web_crawler.requests.get")
    def test_fetch_urls(self, mock_get):
        expected_urls = ["https://test1.com", "https://test2.com"]
        html_content = (
            f'<a href="{expected_urls[0]}"></br></a><a href="{expected_urls[1]}"></a>'
        )
        mock_get.return_value.content = html_content
        urls = fetch_urls(URL)
        self.assertTrue(isinstance(urls, list))
        self.assertEqual(len(urls), 2)
        urls = [url.get("href") for url in urls]
        self.assertEqual(urls, expected_urls)
