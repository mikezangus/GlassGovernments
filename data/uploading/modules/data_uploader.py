from datetime import datetime
from pymongo import GEOSPHERE, UpdateOne


def upload_data(db, data: object, subject, year: str):
    try:
        collection_name = f"{year}x"
        start_time = datetime.now().strftime('%H:%M:%S')
        print(f"{subject} | Started uploading cleaned data to collection {collection_name} at {start_time}")
        collection = db[collection_name]
        collection.create_index([("contribution_location", GEOSPHERE)])
        problem_records = []
        operations = []
        for record in data.to_dict(orient = "records"):
            if not record["transaction_id"]:
                problem_records.append(record)
                continue
            operations.append(UpdateOne(
                {"transaction_id": record["transaction_id"]},
                {"$setOnInsert": record},
                upsert = True
            ))
        if problem_records:
            print(f"{subject} | Problematic records found in file")
            for record in problem_records:
                print(f"{subject} | Missing transaction_id for record: {record}")
        if operations:
            result = collection.bulk_write(operations)
            end_time = datetime.now().strftime('%H:%M:%S')
            print(f"{subject} | Finished uploading {result.upserted_count} new donations to collection {collection_name} at {end_time}")
        else:
            print(f"{subject} | No new donations to upload")
        return
    except Exception as e:
        print(f"{subject} | Failed to upload data. Exception: {e}")
        return