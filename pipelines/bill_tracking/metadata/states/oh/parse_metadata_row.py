from ...utils.create_id import create_id
from ....shared.rows import BillMetadataRow


def _extract_type(row: str) -> str:
    return row.split(' ')[0]


def _extract_num(row: str) -> str:
    return row.split(' ')[1]


def _build_url(session: str, type: str, num: str) -> str:
    return f"https://statusreport.lsc.ohio.gov/legislation/view/{session}?type={type}&number={num}"


def parse_metadata_row(
    raw_row: str,
    session: str,
    state: str
) -> BillMetadataRow:
    type = _extract_type(raw_row)
    num = _extract_num(raw_row)
    url = _build_url(session, type, num)
    metadata = BillMetadataRow(
        id="",
        state=state,
        session=str(session),
        type=type,
        num=num,
        bill_url=url
    )
    metadata.id = create_id(metadata)
    return metadata
