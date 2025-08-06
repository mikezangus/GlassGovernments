from schemas.rows import BillMetadataRow
from states.oh.enums import BillMetadata


def create_row(metadata: BillMetadata) -> BillMetadataRow:
    return {
        "id": f"{metadata.state}_{metadata.session}_{metadata.type}_{metadata.bill_num}",
        "state": metadata.state,
        "session": metadata.session,
        "type": metadata.type,
        "bill_num": metadata.bill_num,
        "bill_url": metadata.bill_url
    }
