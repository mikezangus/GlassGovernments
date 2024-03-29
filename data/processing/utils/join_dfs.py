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


def join_dfs(
    left_df: DataFrame,
    right_df: DataFrame,
    join_col: str,
    join_type: JoinType,
    action: str = None
) -> DataFrame:
    print(f"\nStarted {action}")
    start_count = left_df.count()
    print(f"Item count before join: {start_count:,}")
    df = left_df.join(
        other=right_df,
        on=join_col,
        how=join_type
    )
    print(f"Finished {action}")
    end_count = df.count()
    print(f"Item count after join: {end_count:,}")
    print(f"Filtered out {(start_count - end_count):,} items")
    df.show()
    return df
