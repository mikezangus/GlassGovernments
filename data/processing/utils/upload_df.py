import pandas as pd
from pymongo import MongoClient
from pyspark.sql import DataFrame
from typing import Literal


ModeType = Literal[
    "append",
    "error",
    "ignore",
    "overwrite"
]


def upload_pandas_df(
    collection_name: str,
    uri: str,
    db_name: str,
    df: pd.DataFrame
) -> None:
    count = len(df)
    print(f"\nStarted uploading {count:,} items to collection {collection_name}")
    print(df.head())
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        data_dict = df.to_dict("records")
        collection.insert_many(data_dict)
        print(f"\nFinished uploading {count:,} items to collection {collection_name}")
    except Exception as e:
        print(f"Failed uploading to collection {collection_name}. Error: {e}")
    return


def upload_spark_df(
    collection_name: str,
    uri: str,
    df: DataFrame,
    mode: ModeType
) -> None:
    count = df.count()
    print(f"\nStarted uploading {count:,} items to collection {collection_name}")
    df.show()
    try:
        df.write \
            .format("mongo") \
            .mode(mode) \
            .option("uri", uri) \
            .option("collection", collection_name) \
            .save()
        print(f"Finished uploading {count:,} items to collection {collection_name}")
    except Exception as e:
        print(f"Failed uploading to collection {collection_name}. Error: {e}")
    return


def upload_df(
    collection_name: str,
    uri: str,
    df: pd.DataFrame | DataFrame,
    db_name: str = None,
    mode: ModeType = None
) -> None:
    if isinstance(df, pd.DataFrame):
        upload_pandas_df(collection_name, uri, db_name, df)
    elif isinstance(df, DataFrame):
        upload_spark_df(collection_name, uri, df, mode)
    return
