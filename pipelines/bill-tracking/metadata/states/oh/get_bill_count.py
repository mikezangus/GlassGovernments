from states.oh.enums import LegislationType
from bs4 import BeautifulSoup
from states.oh.construct_search_url import construct_search_url
import requests


def get_bill_count(session: int) -> int:
    url = construct_search_url(session, 1, 10, list(LegislationType))
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    css_selector = "div.search-results-info strong span"
    spans = bs.select(css_selector)
    if spans:
        return int(spans[-1].text.replace(",", ""))
    return 0
