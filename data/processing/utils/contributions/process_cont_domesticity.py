import pandas as pd
from .process_districtwide_conts import process_districtwide_conts
from .process_statewide_conts import process_statewide_conts


def divide_cands(
    cands_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    dist_cands_df = cands_df[
        (cands_df["OFFICE"] == "H") &
        (cands_df["DISTRICT"] != "00")
    ]
    dist_cands_df = dist_cands_df.drop(
        columns=["OFFICE"]
    )
    statewide_cands_df = cands_df[
        (cands_df["OFFICE"] == "S") |
        (cands_df["DISTRICT"] == "00")
    ]
    statewide_cands_df = statewide_cands_df.drop(
        columns=["OFFICE"]
    )
    return dist_cands_df, statewide_cands_df


def process_cont_domesticity(
    cands_df: pd.DataFrame,
    dists_df: pd.DataFrame,
    conts_df: pd.DataFrame
) -> pd.DataFrame:
    districtwide_cands_df, statewide_cands_df = divide_cands(
        cands_df=cands_df
    )
    districtwide_conts_df = process_districtwide_conts(
        cands_df=districtwide_cands_df,
        dists_df=dists_df,
        conts_df=conts_df
    )
    statewide_conts_df = process_statewide_conts(
        cands_df=statewide_cands_df,
        conts_df=conts_df
    )
    return districtwide_conts_df, statewide_conts_df
