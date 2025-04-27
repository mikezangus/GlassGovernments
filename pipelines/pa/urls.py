rss_base_url = "https://legis.state.pa.us/WU01/LI/RSS/"
house_rss_url = rss_base_url + "HouseBills.xml"
senate_rss_url = rss_base_url + "SenateBills.xml"


BILL_TEXT_BASE_URL = "https://palegis.us/legislation/bills/text/HTM/"


def bill_text_url(
    year: str, session: str, bill_type: str, bill_num: str, print_num: str
) -> str:
    bill_num = str(bill_num).zfill(4)
    print_num = str(print_num).zfill(4)
    return BILL_TEXT_BASE_URL + f"{year}/{session}/{bill_type}{bill_num}/PN{print_num}"
