import requests
import click
from bs4 import BeautifulSoup
from http import HTTPStatus


def fetch_urls(url):
    res = requests.get(url)
    if (
        res.status_code != HTTPStatus.OK
        or res.headers.get("content-type") != "text/html"
    ):
        return []

    soup = BeautifulSoup(res.content, "html.parser")
    return soup.find_all("a", href=lambda x: x and x.startswith("http"))


@click.command()
@click.option("--url", required=True, help="Home Page URL")
def main(url):
    urls_to_fetch = [url]
    while True:
        res_urls = set()
        for req_url in urls_to_fetch:
            click.echo("Fetching URLs from {}".format(req_url))
            fetched_urls = fetch_urls(req_url)
            if not fetched_urls:
                click.echo("{} is could be unsupported URL or empty".format(req_url))

            for url in fetched_urls:
                click.echo(f"\t{url.get('href')}")
                res_urls.add(url.get("href"))

        urls_to_fetch = res_urls


if __name__ == "__main__":
    main()
