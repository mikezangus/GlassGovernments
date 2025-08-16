from shared.rows import BillMetadataRow


def _extract_type(row: str) -> str:
    return row.split(' ')[0]


def _extract_num(row: str) -> str:
    return row.split(' ')[1]


def _build_url(session: str, type: str, num: str) -> str:
    return f"https://statusreport.lsc.ohio.gov/legislation/view/{session}?type={type}&number={num}"


def _create_id(state: str, session: str, type: str, num: str) -> str:
    return '_'.join([state, str(session), type, num])


def parse_metadata_row(
    raw_row: str,
    session: str,
    state: str
) -> BillMetadataRow:
    type = _extract_type(raw_row)
    num = _extract_num(raw_row)
    url = _build_url(session, type, num)
    id = _create_id(state, session, type, num)
    return BillMetadataRow(
        id=id,
        state=state,
        session=session,
        type=type,
        num=num,
        bill_url=url
    )
