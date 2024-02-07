from pyspark.sql import DataFrame


def filter_new_items(df_main: DataFrame, df_existing_entries: DataFrame) -> DataFrame:
    if df_existing_entries is not None:
        print("\nStarted filtering out existing items")
        df_start_count = df_main.count()
        df = df_main.join(
            other = df_existing_entries,
            on = "TRAN_ID",
            how = "left_anti"
        )
        df_end_count = df.count()
        print(f"Finished filtering out {(df_start_count - df_end_count):,} existing items")
        return df
    return df_main
