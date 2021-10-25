import requests
import click
from bs4 import BeautifulSoup
from http import HTTPStatus


def fetch_urls(url):
    try:
        res = requests.get(url)

    except Exception:
        return []

    if (
        res.status_code != HTTPStatus.OK
        or "text/html" not in res.headers["content-type"]
    ):
        return []

    soup = BeautifulSoup(res.content, "html.parser")
    return soup.find_all("a", href=lambda x: x and x.startswith("http"))


@click.command()
@click.option("--url", required=True, help="Home Page URL")
@click.option("--depth", default=-1, required=True, help="Recursive length", type=int)
def main(url, depth):
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

        if depth is not None:
            depth -= 1
            if depth == 0:
                break

        urls_to_fetch = res_urls


if __name__ == "__main__":
    main()
