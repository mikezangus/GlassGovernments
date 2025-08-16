from shared.rows import BillMetadataRow
from metadata.states.pa.urls import bill_base_url
from metadata.utils.create_id import create_id
from typing import Callable
from metadata.utils.create_id import create_id


def _extract_from_guid(
    guid: str,
    i: int,
    increment_max: int,
    fn_increment_condition: Callable[[str], bool],
    field_name: str
) -> tuple[str, int]:
    start = i
    while i < increment_max and fn_increment_condition(guid[i]):
        i += 1
    if i == start:
        raise ValueError(f"Failed to extract {field_name} from guid={guid}")
    return guid[start:i], i


def parse_metadata_row(feed_entry: dict[str, any], state: str) -> BillMetadataRow:
    i = 0
    guid = feed_entry["id"]
    guid_len = len(guid)
    session, i = _extract_from_guid(guid, i, 4, str.isdigit, "session")
    special_session, i = _extract_from_guid(guid, i, guid_len, str.isdigit, "special_session")
    type, i = _extract_from_guid(guid, i, guid_len, str.isalpha, "type")
    num, i = _extract_from_guid(guid, i, guid_len, str.isdigit, "bill_num")
    metadata = BillMetadataRow(
        id="",
        state=state,
        session=session,
        type=type,
        num=num,
        bill_url=f"{bill_base_url}{session}/{type}{num}",
        special_session=special_session,
    )
    metadata.id = create_id(metadata)
    return metadata
