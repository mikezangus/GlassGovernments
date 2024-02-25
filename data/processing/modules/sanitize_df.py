from pyspark.sql import DataFrame
from typing import Literal
from .set_cols import set_cand_cols, set_cont_cols


def sanitize_df(df: DataFrame, mode: Literal["cand", "cont"]) -> DataFrame:
    if mode == "cand":
        cols = set_cand_cols("output")
    elif mode == "cont":
        cols = set_cont_cols("output")
    missing_cols = [c for c in cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    df = df.select(*cols)
    return df
