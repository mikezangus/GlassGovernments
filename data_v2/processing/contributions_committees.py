from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, date_format
from pyspark.sql.types import FloatType
from modules.decide_year import decide_year
from modules.get_mongo_uri import get_mongo_uri
from modules.load_df import load_df
from modules.load_filter_df import load_filter_df
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.upload_df import upload_df


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CMTE_ID",
        "ENTITY_TP",
        "ZIP_CODE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "OTHER_ID",
        "CAND_ID",
        "TRAN_ID"
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


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


def main():
    file_type = "pas2"
    year = decide_year()
    uri = get_mongo_uri()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    spark = load_spark(uri)
    df_main = load_df(year, file_type, f"it{file_type}.txt", spark, headers, cols)
    df_candidates = load_filter_df(year, "candidates", spark, uri, "CAND_ID", "Candidates")
    df_existing_entries = load_filter_df(year, "contributions", spark, uri, "TRAN_ID", "Existing Entries")
    df_main = filter_df(df_main, df_candidates, df_existing_entries)
    df_main = format_df(df_main)
    upload_df(year, "contributions_committees", uri, df_main, "append")
    spark.stop()


if __name__ == "__main__":
    main()