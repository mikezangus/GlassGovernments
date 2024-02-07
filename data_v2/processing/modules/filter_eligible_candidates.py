from pyspark.sql import DataFrame


def filter_eligible_candidates(df_main: DataFrame, df_candidates: DataFrame, join_col: str) -> DataFrame:
    print("\nStarted filtering out ineligible candidates")
    df_start_count = df_main.count()
    df = df_main.join(
        other = df_candidates,
        on = join_col,
        how = "inner"
    )
    df_end_count = df.count()
    print(f"Finished filtering out {(df_start_count - df_end_count):,} ineligible candidates")
    return df
