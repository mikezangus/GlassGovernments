import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, lit, struct, to_json, expr

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_locations_file_path


def load_locations_df(spark: SparkSession) -> DataFrame:
    path = os.path.join(get_locations_file_path(), "locations.csv")
    df = spark.read.csv(
        path = path,
        header = True,
        inferSchema=False
    ) \
        .withColumn("LAT", col("LAT").cast("float")) \
        .withColumn("LON", col("LON").cast("float"))
    return df


def convert_zip_codes_to_coordinates(main_df: DataFrame, location_df: DataFrame):
    df = main_df.join(
        other = location_df,
        on = "ZIP",
        how = "inner"
    )
    df = df.withColumn(
        colName = "COORDINATES",
        col = (
            to_json(struct(
                lit("Point").alias("type"),
                struct(
                    col("LON"),
                    col("LAT")
                ).alias("coordinates")
            ))
        )
    )
    return df


def drop_cols(df: DataFrame) -> DataFrame:
    df = df.drop("ZIP", "LAT", "LON")
    return df


def load_coordinates(spark: SparkSession, main_df: DataFrame) -> DataFrame:
    try:
        location_df = load_locations_df(spark)
        df = convert_zip_codes_to_coordinates(main_df, location_df)
        df = drop_cols(df)
        return df
    except Exception:
        return main_df
    