import requests
from bs4 import BeautifulSoup
from metadata.states.oh.urls import bill_url_base


def get_bill_urls(search_url: str) -> list[str]:
    response = requests.get(search_url)
    response.raise_for_status()
    bs = BeautifulSoup(response.text, "html.parser")
    bill_urls = []
    number_cells = bs.find_all("th", class_="number-cell")
    for i in range(len(number_cells)):
        a_tag = number_cells[i].find("a")
        if a_tag and a_tag.has_attr("href"):
            bill_urls.append(f"{bill_url_base}{a_tag["href"]}")
    return bill_urls
