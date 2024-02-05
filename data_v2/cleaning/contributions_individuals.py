import json
import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_raw_dir, get_config_file_path, get_headers_dir, get_src_file_dir


def decide_year() -> str:
    raw_dir = get_raw_dir()
    year_dirs = os.listdir(raw_dir)
    year_options = [y for y in year_dirs if y.isdigit()]
    sorted_year_options = sorted(
        year_options,
        key = lambda x: int(x)
    )
    formatted_year_options = ', '.join(sorted_year_options)
    while True:
        year = input(f"\nFor which year do you want to clean raw data?\nAvailable years: {formatted_year_options}\n> ")
        if year in year_options:
            return year
        else:
            print(f"\n{year} isn't an available year, try again")


def connect_to_mongo():
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    return uri


def load_headers(file_type: str) -> list:
    dir = get_headers_dir()
    path = os.path.join(dir, f"{file_type}_header_file.csv")
    with open(path, "r") as header_file:
        headers = header_file.readline().strip().split(",")
    return headers


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CMTE_ID",
        "ENTITY_TP",
        "ZIP_CODE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "OTHER_ID",
        "TRAN_ID",
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def load_candidates_df(spark: SparkSession, uri: str, year: str):
    print("\nStarted loading Candidates DataFrame\n")
    collection_name = f"{year}_candidate_master"
    df = spark.read.format("mongo") \
        .option("uri", uri) \
        .option("collection", collection_name) \
        .load()
    df = df.select("CMTE_ID")
    print("\nFinished loading Candidates DataFrame")
    print(f"Candidate count: {df.count():,}\n")
    return df


def get_existing_entries(spark: SparkSession, year: str, uri: str) -> SparkDataFrame | None:
    collection_name = f"{year}_individual_contributions"
    try:
        df = spark.read \
            .format("mongo") \
            .option("uri", uri) \
            .option("collection", collection_name) \
            .load()
        if df.limit(1).count() == 0:
            print(f"Collection {collection_name} is empty")
            return None
        else:
            df = df.select("TRAN_ID")
            print(f"Existing entires: {df.count():,}")
            return df
    except Exception as e:
        print(f"Error loading collection {collection_name}. Error: {e}")
        return None


def load_df(year: str, file_type: str, spark: SparkSession, headers: list, cols: list, df_candidates: SparkDataFrame, existing_entries: SparkDataFrame = None) -> SparkDataFrame:
    print("\nStarted loading Full DataFrame\n")
    src_dir = get_src_file_dir(year, file_type)
    src_path = os.path.join(src_dir, "itcont.txt")
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    )
    for i, col_name in enumerate(headers):
        df = df.withColumnRenamed(f"_c{i}", col_name)
    df = df.select(*[headers[index] for index in cols])
    df_filtered = df.join(df_candidates, "CMTE_ID")
    if existing_entries:
        df_filtered = df_filtered.join(
            existing_entries,
            df["TRAN_ID"] == existing_entries["TRAN_ID"],
            "left_anti"
        )
    df_formatted = df_filtered \
        .withColumn(
            "TRANSACTION_AMT",
            df_filtered["TRANSACTION_AMT"].cast(FloatType())
        )\
        .withColumn(
            "TRANSACTION_DT",
            to_date(df_filtered["TRANSACTION_DT"], "MMddyyyy")
        ) \
        .withColumn(
            "TRANSACTION_DT",
            date_format(col("TRANSACTION_DT"), "yyyy-MM-dd")
        )
    print("\nFinished loading Full DataFrame\n")
    return df_formatted


def upload_df(year: str, uri: str, df: SparkDataFrame) -> None:
    collection_name = f"{year}_individual_contributions"
    print(f"\nStarted uploading {df.count():,} entries to collection {collection_name}")
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("uri", uri) \
        .option("collection", collection_name) \
        .save()
    print(f"Finished uploading {df.count():,} entries to collection {collection_name}")
    return


def main():
    file_type = "indiv"
    year = decide_year()
    uri = connect_to_mongo()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = SparkSession.builder \
        .appName("Indiv contributions") \
        .config("spark.mongodb.input.uri", uri) \
        .config("spark.mongodb.output.uri", uri) \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()
    df_candidates = load_candidates_df(spark, uri, year)
    df_existing_entries = get_existing_entries(spark, year, uri)
    df = load_df(year, file_type, spark, headers, cols, df_candidates, df_existing_entries)
    upload_df(year, uri, df)
    spark.stop()


if __name__ == "__main__":
    main()