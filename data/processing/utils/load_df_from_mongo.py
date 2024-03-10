import pandas as pd
from pymongo import MongoClient
from pyspark.sql import SparkSession, DataFrame
from typing import List


def load_spark_df_from_mongo(
    spark: SparkSession,
    uri: str,
    collection_name: str,
    fields: List[str] = None,
    subject: str = None
) -> DataFrame | None:
    print(f"\nStarted loading {subject} Spark DataFrame from Mongo")
    df = spark.read \
        .format("mongo") \
        .option("uri", uri) \
        .option("collection", collection_name) \
        .load()
    if df.limit(1).count() > 0:
        if fields is not None:
            df = df.select(*fields)
        print(f"Finished loading {subject} Spark DataFrame from Mongo")
        print(f"Item count: {df.count():,}")
        df.show()
        return df
    print(f"No data to load for {subject}")
    return


def load_pd_df_from_mongo(
    uri: str,
    db_name: str,
    collection_name: str,
    subject: str = None
) -> pd.DataFrame | None:
    print(f"\nStarted loading {subject} Pandas DataFrame from Mongo")
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        return
    print(f"Finished loading {subject} Pandas DataFrame from Mongo")
    print(f"Item count: {len(df):,}")
    return df
