from pyspark.sql import DataFrame
from typing import Literal


def upload_df(year: str, collection_name: str, uri: str, df: DataFrame, mode: Literal["append", "overwrite", "error", "ignore"]) -> None:
    collection = f"{year}_{collection_name}"
    df_count = f"{df.count():,}"
    print(f"\nStarted uploading {df_count} new items to collection {collection}")
    df.write \
        .format("mongo") \
        .mode(mode) \
        .option("uri", uri) \
        .option("collection", collection) \
        .save()
    print(f"Finished uploading {df_count} new items to collection {collection}")
    return
