import pandas as pd
from pymongo import MongoClient
from pyspark.sql import SparkSession, DataFrame
from typing import Literal


def load_spark_df_from_mongo(
    spark: SparkSession,
    uri: str,
    collection_name: str,
    fields: list=None,
    subject: str=None
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


def load_pandas_df_from_mongo(
    uri: str,
    db_name: str,
    collection_name: str,
    fields: list = None,
    subject: str=None
) -> pd.DataFrame | None:
    print(f"\nStarted loading {subject} Pandas DataFrame from Mongo")
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    if fields is not None:
        projection = {
            field: 1 for field in fields
        }
        projection["_id"] = 0
    else:
        projection = None
    cursor = collection.find({}, projection)
    df = pd.DataFrame(list(cursor))
    if df.empty:
        return
    print(f"Finished loading {subject} Pandas DataFrame from Mongo")
    print(f"Item count: {len(df):,}")
    print(df.head())
    return df


def load_df_from_mongo(
    df_type: Literal["pandas", "spark"],
    uri: str,
    collection_name: str,
    db_name: str=None,
    spark: SparkSession=None,
    fields: list=None,
    subject: str=None
) -> pd.DataFrame | DataFrame:
    if df_type == "pandas":
        return load_pandas_df_from_mongo(uri, db_name, collection_name, fields, subject)
    elif df_type == "spark":
        return load_spark_df_from_mongo(spark, uri, collection_name, fields, subject)
