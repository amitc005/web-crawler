import requests
from bs4 import BeautifulSoup

URL = "http://www.rescale.com"


def main():
    res = requests.get(URL)
    soup = BeautifulSoup(res.content, "html.parser")
    for url in soup.find_all("a", href=lambda x: x and x.startswith("http")):
        print(url.get("href"))


if __name__ == "__main__":
    main()
