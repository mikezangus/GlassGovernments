from ...shared.rows import BillMetadataRow


def create_id(metadata: BillMetadataRow) -> str:
    parts = [metadata.state, metadata.session]
    if metadata.special_session:
        parts.append(metadata.special_session)
    parts.append(metadata.type)
    parts.append(metadata.num)
    return '_'.join(parts)
