from pymongo import GEOSPHERE, UpdateOne


def upload_data(db, data, subject: str, year: str, chamber: str):
    print(f"Starting to upload data for {subject}")
    collection_name = f"{year}_{chamber.lower()}x"
    collection = db[collection_name]
    collection.create_index([("contribution_location", GEOSPHERE)])
    operations = []
    for record in data.to_dict(orient = "records"):
        operations.append(UpdateOne(
            {"transaction_id": record["transaction_id"]},
            {"$setOnInsert": record},
            upsert = True
        ))
    if operations:
        result = collection.bulk_write(operations)
        print(f"Uploaded {result.upserted_count} new donations for {subject} to {collection_name}")
    else:
        print(f"No new records for {subject} to upload")