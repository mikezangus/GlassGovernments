from pyspark.sql import DataFrame


def filter_out_zero_amts(input_df: DataFrame) -> DataFrame:
    print("Started filtering out zero amounts")
    print(f"Items before filtering: {(input_df.count()):,}")
    df = input_df.filter(input_df["TRANSACTION_AMT"] != 0)
    print("Finished filtering out zero amounts")
    print(f"Items after filtering: {(df.count()):,}")
    return df
