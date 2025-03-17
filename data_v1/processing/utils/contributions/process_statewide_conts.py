import pandas as pd


def process_statewide_conts(
    cands_df: pd.DataFrame,
    conts_df: pd.DataFrame
) -> pd.DataFrame:
    df = pd.merge(
        left=cands_df,
        right=conts_df,
        on="CAND_ID",
        how="inner"
    )
    df["DOMESTIC"] = df["CONT_STATE"] == df["STATE"]
    return df
