from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col


def load_locations_df(spark: SparkSession) -> DataFrame:
    df = spark.read \
        .format("mongo") \
        .option("collection", "locations") \
        .load()
    return df


def join_dfs(main_df: DataFrame, location_df: DataFrame) -> DataFrame:
    df = main_df.join(
        other = location_df,
        on = "ZIP",
        how = "left"
    )
    return df


def manage_cols(df: DataFrame) -> DataFrame:
    df = df \
        .withColumn(
            colName = "LOCATION",
            col = col("COORDS")
        ) \
        .drop("_id", "COORDS", "ZIP")
    return df


def main(spark: SparkSession, main_df: DataFrame) -> DataFrame:
    print("\nStarted converting ZIP codes to coordinates")
    location_df = load_locations_df(spark)
    df = join_dfs(main_df, location_df)
    df = manage_cols(df)
    print("Finished converting ZIP codes to coordinates")
    print(f"Item count: {(df.count()):,}")
    df.show()
    return df
