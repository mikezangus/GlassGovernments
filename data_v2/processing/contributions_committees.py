import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType

from modules.decide_year import decide_year
from modules.load_filter_df import load_filter_df
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.get_mongo_uri import get_mongo_uri

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_src_file_dir


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CMTE_ID",
        "ENTITY_TP",
        "NAME",
        "ZIP_CODE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "OTHER_ID",
        "CAND_ID",
        "TRAN_ID"
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def load_df(year: str, file_type: str, spark: SparkSession, headers: list, cols: list) -> DataFrame:
    print("\nStarted loading Full DataFrame\n")
    src_dir = get_src_file_dir(year, file_type)
    src_path = os.path.join(src_dir, f"it{file_type}.txt")
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    )
    for i, col_name in enumerate(headers):
        df = df.withColumnRenamed(f"_c{i}", col_name)
    df = df.select(*[headers[index] for index in cols])
    print(f"\nFinished loading Full DataFrame")
    print(f"Total entries: {df.count():,}")
    return df


def filter_df(df: DataFrame, df_candidates: DataFrame, df_existing_entries: DataFrame) -> DataFrame:
    print(f"\nStarted filtering Full DataFrame\n")
    df_count_full = df.count()
    df = df.join(
        df_candidates,
        "CAND_ID",
        "inner"
    )
    if df_existing_entries is not None:
        df = df.join(
            df_existing_entries,
            df["TRAN_ID"] == df_existing_entries["TRAN_ID"],
            "left_anti"
        )
    df_count_filtered = df.count()
    print(f"\nFinished filtering out {(df_count_full - df_count_filtered):,} entries")
    return df


def format_df(df: DataFrame) -> DataFrame:
    print(f"\nStarted formatting Full DataFrame")
    df = df \
        .withColumn(
            "TRANSACTION_AMT",
            df["TRANSACTION_AMT"].cast(FloatType())
        ) \
        .withColumn(
            "TRANSACTION_DT",
            to_date(df["TRANSACTION_DT"], "MMddyyyy")
        ) \
        .withColumn(
            "TRANSACTION_DT",
            date_format(col("TRANSACTION_DT"), "yyyy-MM-dd")
        )
    print("\nFinished formatting Full DataFrame\n")
    return df


def upload_df(year: str, uri: str, df: DataFrame) -> None:
    collection_name = f"{year}_committee_contributions"
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
    file_type = "pas2"
    year = decide_year()
    uri = get_mongo_uri()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = load_spark(uri)
    df_main = load_df(year, file_type, spark, headers, cols)
    df_candidates = load_filter_df(year, "candidates", spark, uri, "CAND_ID", "Candidates")
    df_existing_entries = load_filter_df(year, "committee_contributions", spark, uri, "TRAN_ID", "Existing Entries")
    df_main = filter_df(df_main, df_candidates, df_existing_entries)
    df_main = format_df(df_main)
    upload_df(year, uri, df_main)
    spark.stop()


if __name__ == "__main__":
    main()