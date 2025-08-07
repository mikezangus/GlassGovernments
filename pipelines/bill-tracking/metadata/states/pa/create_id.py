from typing import Callable


def _extract_field(
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


def create_id(guid: str) -> str:
    idx = 0
    guid_len = len(guid)
    session, idx = _extract_field(guid, idx, 4, str.isdigit, "session")
    special_session, idx = _extract_field(guid, idx, guid_len, str.isdigit, "special_session")
    type, idx = _extract_field(guid, idx, guid_len, str.isalpha, "type")
    bill_num, idx = _extract_field(guid, idx, guid_len, str.isdigit, "bill_num")
    _, idx = _extract_field(guid, idx, guid_len, str.isalpha, "skipping 'PN'")
    print_num, _ = _extract_field(guid, idx, guid_len, str.isdigit, "print_num")
    return f"PA_{session}_{special_session}_{type}_{bill_num}_{print_num}"
