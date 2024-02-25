from pyspark.sql import DataFrame
from typing import Literal


JoinType = Literal[
    "inner",
    "cross",
    "outer",
    "full", "fullouter", "full_outer",
    "left", "leftouter", "left_outer",
    "right", "rightouter", "right_outer",
    "semi", "leftsemi", "left_semi",
    "anti", "leftanti", "left_anti"
]


def join_dfs(df1: DataFrame, df2: DataFrame, join_col: str, join_type: JoinType, action: str) -> DataFrame:
    print(f"\nStarted {action}")
    print(f"Item count before join: {(df1.count()):,}")
    df = df1.join(
        other = df2,
        on = join_col,
        how = join_type
    )
    print(f"Finished {action}")
    print(f"Item count after join: {(df.count()):,}")
    return df
