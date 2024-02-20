from pyspark.sql import DataFrame


def filter_out_ineligible_candidates(main_df: DataFrame, candidates_df: DataFrame, join_col: str) -> DataFrame:
    print("\nStarted filtering out ineligible candidates' items")
    df_start_count = main_df.count()
    df = main_df.join(
        other = candidates_df,
        on = join_col,
        how = "inner"
    )
    df_end_count = df.count()
    print(f"Finished filtering out {(df_start_count - df_end_count):,} ineligible candidates' items")
    print(f"Item count: {df_end_count:,}")
    return df
