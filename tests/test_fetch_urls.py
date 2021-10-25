import unittest
from unittest.mock import patch
from web_crawler import fetch_urls
from http import HTTPStatus

URL = "https://test.com"


class TestFetchURls(unittest.TestCase):
    HTML_MIME_TYPE = "text/html; charset=utf-8"

    @patch("web_crawler.requests.get")
    def test_fetch_urls(self, mock_get):
        expected_urls = ["https://test1.com", "https://test2.com"]
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.headers = {"content-type": self.HTML_MIME_TYPE}

        html_content = (
            f'<a href="{expected_urls[0]}"></br></a><a href="{expected_urls[1]}"></a>'
        )
        mock_get.return_value.content = html_content
        urls = fetch_urls(URL)
        self.assertTrue(isinstance(urls, list))
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls, expected_urls)

    @patch("web_crawler.requests.get")
    def test_fetch_urls_with_unsuccess_response_code(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.headers = {"content-type": self.HTML_MIME_TYPE}
        urls = fetch_urls(URL)
        self.assertTrue(isinstance(urls, list))
        self.assertEqual(len(urls), 0)

    @patch("web_crawler.requests.get")
    def test_fetch_urls_with_unknown_mime_type(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.headers = {"content-type": "unknown"}
        urls = fetch_urls(URL)
        self.assertTrue(isinstance(urls, list))
        self.assertEqual(len(urls), 0)

    @patch("web_crawler.requests.get")
    def test_fetch_urls_with_exception(self, mock_get):
        mock_get.side_effect = Exception()
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.headers = {"content-type": self.HTML_MIME_TYPE}

        urls = fetch_urls(URL)
        self.assertTrue(isinstance(urls, list))
        self.assertEqual(len(urls), 0)
