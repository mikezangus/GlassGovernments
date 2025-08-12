from shared.rows import BillMetadataRow
from metadata.states.pa.urls import bill_base_url
from metadata.utils.create_id import create_id
from typing import Callable
from metadata.utils.create_id import create_id


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


def extract_metadata(feed_entry: dict[str, any], state: str) -> BillMetadataRow:
    idx = 0
    guid = feed_entry["id"]
    guid_len = len(guid)
    session, idx = _extract_from_guid(guid, idx, 4, str.isdigit, "session")
    special_session, idx = _extract_from_guid(guid, idx, guid_len, str.isdigit, "special_session")
    type, idx = _extract_from_guid(guid, idx, guid_len, str.isalpha, "type")
    num, idx = _extract_from_guid(guid, idx, guid_len, str.isdigit, "bill_num")
    metadata = BillMetadataRow(
        id="",
        state=state,
        session=session,
        special_session=special_session,
        type=type,
        num=num,
        bill_url=f"{bill_base_url}{session}/{type}{num}"
    )
    metadata.id = create_id(metadata)
    return metadata
