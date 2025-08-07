from schemas.rows import BillMetadata


def create_id(metadata: BillMetadata) -> str:
    parts = [metadata.state, metadata.session]
    if metadata.special_session:
        parts.append(metadata.special_session)
    parts.append(metadata.type)
    parts.append(metadata.bill_num)
    if metadata.print_num:
        parts.append(metadata.print_num)
    return "_".join(parts)
