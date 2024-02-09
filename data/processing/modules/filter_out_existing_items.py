from pyspark.sql import DataFrame


def filter_out_existing_items(main_df: DataFrame, existing_items_df: DataFrame) -> DataFrame:
    if existing_items_df is not None:
        print("\nStarted filtering out existing items")
        df_start_count = main_df.count()
        df = main_df.join(
            other = existing_items_df,
            on = "TRAN_ID",
            how = "left_anti"
        )
        df_end_count = df.count()
        print(f"Finished filtering out {(df_start_count - df_end_count):,} existing items")
        return df
    return main_df
