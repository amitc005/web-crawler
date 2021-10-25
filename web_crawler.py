import requests
import click
from bs4 import BeautifulSoup
from http import HTTPStatus
import concurrent.futures


def fetch_urls(url):
    try:
        res = requests.get(url)

    except Exception as e:
        click.echo(f"Error: {e}")
        return []

    if (
        res.status_code != HTTPStatus.OK
        or "text/html" not in res.headers["content-type"]
    ):
        click.echo(f"Error: {url}")
        return []

    soup = BeautifulSoup(res.content, "html.parser")
    return [
        anchor_tag.get("href")
        for anchor_tag in soup.find_all("a", href=lambda x: x and x.startswith("http"))
    ]


def display_urls(req_url, data):
    click.echo("Fetching URLs from {}".format(req_url))
    for url in data:
        click.echo(f"\t{url}")


@click.command()
@click.option("--url", required=True, help="Home Page URL")
@click.option("--depth", default=-1, required=True, help="Recursive length", type=int)
def main(url, depth):
    urls_to_fetch = [url]

    while True:
        res_urls = set()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(urls_to_fetch)
        ) as executor:
            future_to_url = {
                executor.submit(fetch_urls, url): url for url in urls_to_fetch
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                res_urls = future.result()
                display_urls(url, res_urls)

            if depth is not None:
                depth -= 1
                if depth == 0:
                    break

            urls_to_fetch = res_urls


if __name__ == "__main__":
    main()
