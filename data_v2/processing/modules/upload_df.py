from pyspark.sql import DataFrame as SparkDataFrame


def upload_df(year: str, collection_name: str, uri: str, df: SparkDataFrame) -> None:
    collection = f"{year}_{collection_name}"
    print(f"\nStarted uploading {df.count():,} entries to collection {collection}")
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("uri", uri) \
        .option("collection", collection_name) \
        .save()
    print(f"\nFinished uploading {df.count():,} entries to collection {collection}")
    return