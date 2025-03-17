import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from .data_types import DataType
from .set_cols import set_cols


def sanitize_pandas_df(
    input_df: pd.DataFrame,
    cols: list
) -> pd.DataFrame:
    print(f"Item count: {len(input_df):,}")
    df = input_df.dropna(subset = cols)
    df = df[cols]
    print("Finished sanitizing DataFrame")
    print(f"Item count: {len(df):,}")
    return df


def sanitize_spark_df(
    input_df: DataFrame,
    cols: list
) -> DataFrame:
    print(f"Item count: {input_df.count():,}")
    input_df.show()
    filter_condition = None
    for c in cols:
        if filter_condition is None:
            filter_condition = col(c).isNotNull()
        else:
            filter_condition = filter_condition & col(c).isNotNull()
    df = input_df.filter(filter_condition)
    df = df.select(*cols)
    print("Finished sanitizing DataFrame")
    print(f"Item count: {df.count():,}")
    return df


def sanitize_df(
    type: DataType,
    df: pd.DataFrame | DataFrame
) -> pd.DataFrame | DataFrame:
    print("\nStarted sanitizing DataFrame")
    cols = set_cols(type, "output")
    missing_cols = [
        c for c in cols if c not in df.columns
    ]
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_cols)}"
        )
    if isinstance(df, pd.DataFrame):
        return sanitize_pandas_df(df, cols)
    elif isinstance(df, DataFrame):
        return sanitize_spark_df(df, cols)
