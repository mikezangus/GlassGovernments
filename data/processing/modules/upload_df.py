from pyspark.sql import DataFrame
from pyspark.sql.utils import AnalysisException
from typing import Literal


def upload_df(collection: str, uri: str, df: DataFrame, mode: Literal["append", "overwrite", "error", "ignore"]) -> None:
    print(f"\nStarted uploading {df.count():,} items to collection {collection}")
    try:
        df.write \
            .format("mongo") \
            .mode(mode) \
            .option("uri", uri) \
            .option("collection", collection) \
            .save()
        print(f"Finished uploading items to collection {collection}")
        return
    except AnalysisException as e:
        print("ERROR:", e)
