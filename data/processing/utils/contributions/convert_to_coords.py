import os
import sys
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRIBUTION_UTILS_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(CONTRIBUTION_UTILS_DIR)
from join_dfs import join_dfs
from load_df_from_mongo import load_spark_df_from_mongo


def manage_cols(df: DataFrame) -> DataFrame:
    df = df \
        .withColumn(
            colName = "LOCATION",
            col = col("COORDS")
        ) \
        .drop("_id", "COORDS", "ZIP")
    return df


def convert_to_coords(spark: SparkSession, uri: str, main_df: DataFrame) -> DataFrame:
    location_df = load_spark_df_from_mongo(
        spark,
        uri,
        "locations",
        ["COORDS", "ZIP"],
        "Locations"
    )
    df = join_dfs(
        main_df,
        location_df,
        "ZIP",
        "left",
        "Converting ZIP codes to coordinates"
    )
    df = manage_cols(df)
    return df
