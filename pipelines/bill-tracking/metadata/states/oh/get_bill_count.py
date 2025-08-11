import requests
from bs4 import BeautifulSoup
from metadata.states.oh.construct_search_url import construct_search_url
from metadata.states.oh.enums import LegislationType


def get_bill_count(session: int) -> int:
    url = construct_search_url(session, 1, 10, list(LegislationType))
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    css_selector = "div.search-results-info strong span"
    spans = bs.select(css_selector)
    if spans:
        return int(spans[-1].text.replace(",", ""))
    return 0
