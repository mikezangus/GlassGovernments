import pandas as pd
from pyspark.sql import DataFrame


def filter_out_existing_items_pandas(
    main_df: pd.DataFrame,
    existing_items_df: pd.DataFrame,
    cols: list
) -> pd.DataFrame:
    print("COLS", cols)
    df = pd.merge(
        main_df,
        existing_items_df[cols],
        on = cols,
        how = "left",
        indicator = True
    )
    df = df[
        df["_merge"] == "left_only"
    ].drop(
        columns = ["_merge"]
    )
    return df


def filter_out_existing_items(
    main_df: DataFrame,
    existing_items_df: DataFrame,
    cols: list
) -> DataFrame:
    print("\nStarted filtering out existing items")
    print(f"Item count: {main_df.count():,}")
    main_df = main_df.select(
        cols + [c for c in main_df.columns if c not in cols]
    )
    existing_items_df = existing_items_df.select(cols)
    df = main_df.join(
        other = existing_items_df,
        on = cols,
        how = "left_anti"
    )
    print("Finished filtering out existing items")
    print(f"Item count: {df.count():,}")
    return df


def filter_out_existing_items(
    main_df: pd.DataFrame | DataFrame,
    existing_items_df: pd.DataFrame | DataFrame,
    cols: list
) -> pd.DataFrame | DataFrame:
    if isinstance(main_df, pd.DataFrame) and isinstance(existing_items_df, pd.DataFrame):
        return filter_out_existing_items_pandas(main_df, existing_items_df, cols)
    elif isinstance(main_df, DataFrame) and isinstance(existing_items_df, DataFrame):
        return filter_out_existing_items(main_df, existing_items_df, cols)
    else:
        raise ValueError("Incorrect or mismatching types for input DataFrames")
