from shared.rows import BillMetadataRow


def create_id(metadata: BillMetadataRow) -> str:
    parts = [
        metadata.state,
        metadata.session,
        metadata.special_session,
        metadata.type,
        metadata.num
    ]
    return '_'.join(parts)
