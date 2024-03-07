import pandas as pd
from pymongo import MongoClient


def load_df_from_mongo(uri: str, db_name: str, collection_name: str) -> pd.DataFrame | None:

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    cursor = collection.find({ })
    df = pd.DataFrame(list(cursor))

    if not df.empty:
        return df
    else:
        return None

