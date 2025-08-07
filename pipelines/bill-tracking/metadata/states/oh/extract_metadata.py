import re
from schemas.rows import BillMetadataRow


def extract_metadata(bill_url: str) -> BillMetadataRow:
    regex_split_text_and_nums = r"([a-zA-Z]+)(\d+)"
    parts = bill_url.strip('/').split('/')
    match = re.match(regex_split_text_and_nums, parts[-1])
    if not match:
        raise RuntimeError()
    session = parts[-2]
    type = match.group(1).upper()
    bill_num = match.group(2)
    return BillMetadataRow(
        state="OH",
        session=session,
        type=type,
        bill_num=bill_num,
        bill_url=bill_url
    )
