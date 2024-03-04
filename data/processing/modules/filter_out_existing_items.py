from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def filter_out_existing_items(main_df: DataFrame, existing_items_df: DataFrame, cols: list) -> DataFrame:
    existing_items_df = existing_items_df.select(cols)
    main_df = main_df.select(
        cols + [c for c in main_df.columns if c not in cols]
    )
    df = main_df.join(
        other = existing_items_df,
        on = cols,
        how = "left_anti"
    )
    return df