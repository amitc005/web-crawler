import requests
import click
from bs4 import BeautifulSoup


def fetch_urls(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup.find_all("a", href=lambda x: x and x.startswith("http"))


@click.command()
@click.option("--url", required=True, help="Home Page URL")
def main(url):
    urls_to_fetch = [url]
    while True:
        res_urls = set()

        for url in urls_to_fetch:
            for url in fetch_urls(url):
                click.echo("Fetching URLs from {}".format(url))
                click.echo(f"\t{url.get('href')}")
                res_urls.add(url.get("href"))

        urls_to_fetch = res_urls


if __name__ == "__main__":
    main()
