from schemas.rows import BillMetadata
from states.pa.create_id import create_id
from states.pa.urls import bill_base_url
from typing import Callable
from utils.create_id import create_id


def _extract_from_guid(
    guid: str,
    idx: int,
    increment_max: int,
    fn_increment_condition: Callable[[str], bool],
    field_name: str
) -> tuple[str, int]:
    start = idx
    while idx < increment_max and fn_increment_condition(guid[idx]):
        idx += 1
    if idx == start:
        raise ValueError(f"Failed to extract {field_name} from guid={guid}")
    return guid[start:idx], idx


def extract_metadata(feed_entry: dict[str, any], state: str) -> BillMetadata:
    idx = 0
    guid = feed_entry["id"]
    guid_len = len(guid)
    session, idx = _extract_from_guid(guid, idx, 4, str.isdigit, "session")
    special_session, idx = _extract_from_guid(guid, idx, guid_len, str.isdigit, "special_session")
    bill_type, idx = _extract_from_guid(guid, idx, guid_len, str.isalpha, "type")
    bill_num, idx = _extract_from_guid(guid, idx, guid_len, str.isdigit, "bill_num")
    _, idx = _extract_from_guid(guid, idx, guid_len, str.isalpha, "skipping 'PN'")
    print_num, _ = _extract_from_guid(guid, idx, guid_len, str.isdigit, "print_num")
    metadata = BillMetadata(
        id="",
        state=state,
        session=session,
        special_session=special_session,
        type=bill_type,
        bill_num=bill_num,
        print_num=print_num,
        bill_url=f"{bill_base_url}{session}/{bill_type}{bill_num}",
        text_url=feed_entry.get("link"),
    )
    metadata.id = create_id(metadata)
    return metadata
