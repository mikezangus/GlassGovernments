from pyspark.sql import DataFrame


def filter_out_zero_amts(df: DataFrame) -> DataFrame:
    print("Started filtering out zero amounts")
    print(f"Items before filtering: {(df.count()):,}")
    df = df.filter(df["TRANSACTION_AMT"] != 0)
    print("Finished filtering out zero amounts")
    print(f"Items after filtering: {(df.count()):,}")
    return df
