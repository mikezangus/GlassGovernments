import os
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.functions import col
import sys
from connect_to_mongo import connect_to_mongo
from decide_year import decide_year
from load_headers import load_headers
from load_spark import load_spark

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_src_file_dir


def get_existing_entries(spark: SparkSession, year: str, uri: str) -> SparkDataFrame | None:
    collection_name = f"{year}_candidate_master"
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
            df = df.select("CAND_ID")
            print(f"Existing entires: {df.count():,}")
            return df
    except Exception as e:
        print(f"Error loading collection {collection_name}. Error: {e}")
        return None


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CAND_ID",
        "CAND_NAME",
        "CAND_PTY_AFFILIATION",
        "CAND_ELECTION_YR",
        "CAND_OFFICE_ST",
        "CAND_OFFICE",
        "CAND_OFFICE_DISTRICT",
        "CAND_ICI",
        "CAND_STATUS",
        "CAND_PCC"
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def load_df(year: str, file_type: str, spark: SparkSession, headers: list, cols: list) -> SparkDataFrame:
    src_dir = get_src_file_dir(year, file_type)
    src_path = os.path.join(src_dir, f"{file_type}.txt")
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    ).toDF(*headers)
    df = df.select(*[headers[index] for index in cols])
    return df


def filter_df(df: SparkDataFrame, year: str) -> SparkDataFrame:
    df = df.filter(
        (col("CAND_ELECTION_YR") == year) &
        (col("CAND_STATUS") == "C")
    )
    return df


def rename_cols(df: SparkDataFrame) -> SparkDataFrame:
    df = df \
        .withColumnRenamed("CAND_NAME", "NAME") \
        .withColumnRenamed("CAND_PTY_AFFILIATION", "PARTY") \
        .withColumnRenamed("CAND_ELECTION_YR", "ELECTION_YEAR") \
        .withColumnRenamed("CAND_OFFICE_ST", "STATE") \
        .withColumnRenamed("CAND_OFFICE", "OFFICE") \
        .withColumnRenamed("CAND_OFFICE_DISTRICT", "DISTRICT") \
        .withColumnRenamed("CAND_ICI", "ICI") \
        .withColumnRenamed("CAND_PCC", "CMTE_ID")
    return df



def upload_df(year: str, uri: str, df: SparkDataFrame) -> None:
    collection_name = f"{year}_candidate_master"
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
    file_type = "cn"
    year = decide_year()
    uri = connect_to_mongo()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = load_spark(uri)
    df = load_df(year, file_type, spark, headers, cols)
    df = filter_df(df, year)
    df = rename_cols(df)
    upload_df(year, uri, df)
    spark.stop()


if __name__ == "__main__":
    main()