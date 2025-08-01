import re


def extract_metadata_from_bill_url(bill_url: str):
    regex_split_text_and_nums = r"([a-zA-Z]+)(\d+)"
    parts = bill_url.strip('/').split('/')
    match = re.match(regex_split_text_and_nums, parts[-1])
    if not match:
        raise RuntimeError()
    session = parts[-2]
    bill_type = match.group(1).upper()
    bill_num = match.group(2)
    return "OH", session, bill_type, bill_num
