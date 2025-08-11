import re
from shared.lib.regexes import regex_split_text_and_nums
from shared.rows import BillMetadataRow
from metadata.utils.create_id import create_id


def extract_metadata(bill_url: str, state: str) -> BillMetadataRow:
    bill_url_parts = bill_url.strip('/').split('/')
    session = bill_url_parts[-2]
    regex_match = re.match(regex_split_text_and_nums, bill_url_parts[-1])
    if not regex_match:
        raise ValueError(f"Failed to split text and nums for {bill_url_parts[-1]}")
    type = regex_match.group(1).upper()
    bill_num = regex_match.group(2)
    metadata = BillMetadataRow(
        id="",
        state=state,
        session=session,
        type=type,
        num=bill_num,
        bill_url=bill_url
    )
    metadata.id = create_id(metadata)
    return metadata
