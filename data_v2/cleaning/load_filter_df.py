from pyspark.sql import SparkSession, DataFrame as SparkDataFrame


def load_filter_df(year: str, collection_name: str, spark: SparkSession, uri: str, id: str) -> SparkDataFrame:
    collection = f"{year}_{collection_name}"
    df = spark.read \
        .format("mongo") \
        .option("uri", uri) \
        .option("collection", collection) \
        .load()
    if df.limit(1).count() > 0:
        df = df.select(id)
        print(f"Filter DataFrame entry count: {df.count():,}")
        return df
    print(f"{collection} is empty or doesn't exist")
    return None