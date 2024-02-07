from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType
from modules.decide_year import decide_year
from modules.filter_eligible_candidates import filter_eligible_candidates
from modules.filter_new_items import filter_new_items
from modules.get_mongo_uri import get_mongo_uri
from modules.load_df import load_df
from modules.load_headers import load_headers
from modules.load_mongo_df import load_mongo_df
from modules.load_spark import load_spark
from modules.rename_contribution_cols import rename_cols
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


def enrich_df(df_main: DataFrame, df_candidates: DataFrame) -> DataFrame:
    df = df_main.join(
        df_candidates.select("CMTE_ID", "CAND_ID"),
        on = "CMTE_ID",
        how = "left"
    )
    return df


def format_df(df: DataFrame) -> DataFrame:
    print("\nStarted formatting DataFrame")
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
    print("Finished formatting DataFrame")
    return df


def main():
    file_type = "indiv"
    year = decide_year()
    uri = get_mongo_uri()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = load_spark(uri)
    df_candidates = load_mongo_df(year, "candidates", spark, uri, "Candidates", "CMTE_ID", "CAND_ID")
    df_existing_entries = load_mongo_df(year, "contributions", spark, uri, "Existing Items", "TRAN_ID")
    df_main = load_df(year, file_type, "itcont.txt", spark, headers, cols)
    df_main = filter_eligible_candidates(df_main, df_candidates, "CMTE_ID")
    df_main = filter_new_items(df_main, df_existing_entries)
    df_main = enrich_df(df_main, df_candidates)
    df_main = format_df(df_main)
    df_main = rename_cols(df_main)
    upload_df(year, "contributions", uri, df_main, "append")
    spark.stop()


if __name__ == "__main__":
    main()
