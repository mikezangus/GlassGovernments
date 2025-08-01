from enums import LegislationType
from bs4 import BeautifulSoup
from construct_search_url import construct_search_url
import requests


def get_bill_count(general_assembly: int) -> int:
    url = construct_search_url(general_assembly, 1, 10, list(LegislationType))
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    css_selector = "div.search-results-info strong span"
    spans = bs.select(css_selector)
    if spans:
        return int(spans[-1].text.replace(",", ""))
    return 0
