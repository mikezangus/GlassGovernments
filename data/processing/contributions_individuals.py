from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType
from modules.decide_year import decide_year
from modules.filter_out_ineligible_candidates import filter_out_ineligible_candidates
from modules.filter_out_existing_items import filter_out_existing_items
from modules.get_mongo_uri import get_mongo_uri
from modules.load_coordinates import main as load_coordinates
from modules.load_df import load_df
from modules.load_headers import load_headers
from modules.load_mongo_df import load_mongo_df
from modules.load_spark import load_spark
from modules.rename_cols import rename_cols
from modules.upload_df import upload_df


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


def main():
    file_type = "indiv"
    year = decide_year()
    uri = get_mongo_uri()
    spark = load_spark(uri)
    candidates_df = load_mongo_df(year, "candidates", spark, uri, "Candidates", "CMTE_ID", "CAND_ID")
    existing_items_df = load_mongo_df(year, "contributions", spark, uri, "Existing Items", "TRAN_ID")
    headers = load_headers(file_type)
    cols = set_cols(headers)
    main_df = load_df(year, file_type, "itcont.txt", spark, headers, cols)
    main_df = filter_out_ineligible_candidates(main_df, candidates_df, "CMTE_ID")
    main_df = filter_out_existing_items(main_df, existing_items_df)
    main_df = enrich_df(main_df, candidates_df)
    main_df = format_df(main_df)
    main_df = rename_cols(main_df)
    main_df = load_coordinates(spark, main_df)
    upload_df(year, "contributions", uri, main_df, "append")
    spark.stop()


if __name__ == "__main__":
    main()
