from pyspark.sql import SparkSession, DataFrame


def load_df_from_mongo(spark: SparkSession, uri: str, collection: str, subject: str, field_1: str = None, field_2: str = None) -> DataFrame | None:
    print(f"\nStarted loading {subject} DataFrame from Mongo collection {collection}")
    df = spark.read \
        .format("mongo") \
        .option("uri", uri) \
        .option("collection", collection) \
        .load()
    if df.limit(1).count() > 0:
        if field_1 and field_2:
            df = df.select(field_1, field_2)
        elif field_1:
            df = df.select(field_1)
        print(f"Finished loading {subject} DataFrame from Mongo")
        print(f"Item count: {(df.count()):,}")
        df.show()
        return df
    print(f"{collection} is empty or doesn't exist")
    return
