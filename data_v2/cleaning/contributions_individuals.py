import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType

from decide_year import decide_year
from load_filter_df import load_filter_df
from load_headers import load_headers
from load_spark import load_spark
from connect_to_mongo import connect_to_mongo

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_src_file_dir


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


def load_df(year: str, file_type: str, spark: SparkSession, headers: list, cols: list) -> SparkDataFrame:
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
    print(f"\nFinished loading Full DataFrame")
    print(f"Total entries: {df.count():,}")
    return df


def filter_df(df: SparkDataFrame, df_candidates: SparkDataFrame, df_existing_entries: SparkDataFrame) -> SparkDataFrame:
    print(f"\nStarted filtering Full DataFrame\n")
    df_count_full = df.count()
    df_filtered = df.join(
        df_candidates,
        "CMTE_ID",
        "inner"
    )
    if df_existing_entries is not None:
        df_filtered = df_filtered.join(
            df_existing_entries,
            df_filtered["TRAN_ID"] == df_existing_entries["TRAN_ID"],
            "left_anti"
        )
    df_count_filtered = df_filtered.count()
    print(f"\nFinished filtering out {(df_count_full - df_count_filtered):,} entries")
    return df_filtered


def format_df(df: SparkDataFrame) -> SparkDataFrame:
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
    spark = load_spark(uri)
    df = load_df(year, file_type, spark, headers, cols)
    df_candidates = load_filter_df(year, "candidate_master", spark, uri, "CMTE_ID")
    df_existing_entries = load_filter_df(year, "individual_contributions", spark, uri, "TRAN_ID")
    df = filter_df(df, df_candidates, df_existing_entries)
    df = format_df(df)
    upload_df(year, uri, df)
    spark.stop()


if __name__ == "__main__":
    main()