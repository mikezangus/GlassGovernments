import pandas as pd
from pymongo import MongoClient


def upload_df_to_mongo(uri: str, db_name: str, collection_name: str, df: pd.DataFrame) -> pd.DataFrame | None:

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)
    client.close()

    if not df.empty:
        return df
    else:
        return None

