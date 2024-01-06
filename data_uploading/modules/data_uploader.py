from pymongo import GEOSPHERE, UpdateOne


def upload_data(db, data, subject: str, year: str, chamber: str):
    try:
        collection_name = f"{year}_{chamber.lower()}x"
        print(f"{subject} | Starting to upload cleaned data to collection {collection_name}")
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
            print(f"{subject} | Finished uploading {result.upserted_count} new donations to collection {collection_name}")
        else:
            print(f"{subject} | No new donations to upload")
        return
    except Exception as e:
        print(f"{subject} | Failed to upload data. Exception: {e}")
        return