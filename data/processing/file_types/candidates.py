import os
import sys
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from modules.decide_year import decide_year
from modules.get_mongo_uri import get_mongo_uri
from modules.load_df_from_file import load_df_from_file
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.load_state_codes import load_usa_state_codes
from modules.upload_df import upload_df


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


def filter_df(df: DataFrame, year: str) -> DataFrame:
    usa_state_codes = load_usa_state_codes()
    df = df.filter(
        (col("CAND_ELECTION_YR") == year) &
        (col("CAND_STATUS") == "C") &
        (col("CAND_OFFICE") != "P") &
        (col("CAND_OFFICE_ST").isin(usa_state_codes))
    )
    df = df.drop("CAND_STATUS")
    return df


def rename_cols(df: DataFrame) -> DataFrame:
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


def update_districts(df: DataFrame) -> DataFrame:
    df = df \
        .withColumn(
            "DISTRICT",
            when(
                col("OFFICE") != "H",
                col("OFFICE")
            ).otherwise(col("DISTRICT")))
    return df


def process_candidates(year: str = None):
    print(f"\n{'-' * 100}\n{'-' * 100}\nStarted processing Candidates")
    file_type = "cn"
    if not year:
        year = decide_year()
    uri = get_mongo_uri()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = load_spark(uri)
    df = load_df_from_file(year, file_type, f"{file_type}.txt", spark, headers, cols)
    df = filter_df(df, year)
    df = rename_cols(df)
    df = update_districts(df)
    upload_df(f"{year}_candidates", uri, df, "overwrite")
    spark.stop()
    print(f"\nFinished processing Candidates\n{'-' * 100}\n{'-' * 100}\n")


if __name__ == "__main__":
    process_candidates(True)