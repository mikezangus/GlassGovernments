import os
import sys
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from modules.decide_year import decide_year
from modules.filter_out_ineligible_candidates import filter_out_ineligible_candidates
from modules.filter_out_existing_items import filter_out_existing_items
from modules.get_mongo_uri import get_mongo_uri
from modules.convert_to_coords import main as convert_to_coords
from modules.load_df_from_file import load_df_from_file
from modules.load_headers import load_headers
from modules.load_df_from_mongo import load_df_from_mongo
from modules.load_spark import load_spark
from modules.rename_cols import rename_cols
from modules.upload_df import upload_df


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CMTE_ID",
        "ENTITY_TP",
        "CITY",
        "STATE",
        "ZIP_CODE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "OTHER_ID",
        "TRAN_ID",
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def enrich_df(main_df: DataFrame, candidates_df: DataFrame) -> DataFrame:
    df = main_df.join(
        other = candidates_df.select("CMTE_ID", "CAND_ID"),
        on = "CMTE_ID",
        how = "left"
    )
    return df


def format_df(df: DataFrame) -> DataFrame:
    print("\nStarted formatting Main DataFrame")
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
    print("Finished formatting Main DataFrame")
    return df


def process_individual_contributions(year: str = None):
    print(f"\n{'-' * 100}\n{'-' * 100}\nStarted processing Individual Contributions")
    file_type = "indiv"
    if not year:
        year = decide_year()
    uri = get_mongo_uri()
    spark = load_spark(uri)
    candidates_df = load_df_from_mongo(spark, uri, f"{year}_candidates", "Candidates", "CMTE_ID", "CAND_ID")
    existing_items_df = load_df_from_mongo(spark, uri, f"{year}_contributions", "Existing Items", "TRAN_ID")
    headers = load_headers(file_type)
    cols = set_cols(headers)
    main_df = load_df_from_file(year, file_type, "itcont.txt", spark, headers, cols)
    main_df = filter_out_ineligible_candidates(main_df, candidates_df, "CMTE_ID")
    main_df = filter_out_existing_items(main_df, existing_items_df)
    main_df = enrich_df(main_df, candidates_df)
    main_df = format_df(main_df)
    main_df = rename_cols(main_df)
    main_df = convert_to_coords(spark, main_df)
    upload_df(f"{year}_contributions", uri, main_df, "append")
    spark.stop()
    print(f"\nFinished processing Individual Contributions\n{'-' * 100}\n{'-' * 100}\n")


if __name__ == "__main__":
    process_individual_contributions(True)
