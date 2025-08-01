
from get_bill_count import get_bill_count
from construct_search_url import construct_search_url
from enums import LegislationType

def run_oh():
    bill_count = get_bill_count(136)
    search_urls = []
    for i in range(1, bill_count + 1, 1000):
        search_urls.append(construct_search_url(136, i, 1000, list(LegislationType)))
    print(search_urls)



if __name__ == "__main__":
    run_oh()
