import geopandas as gpd
import os
import pandas as pd
import sys
from shapely.geometry import mapping
from typing import Literal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PROCESSING_DIR)
from utils.filter_out_existing_items import filter_out_existing_items
from utils.get_mongo_config import get_mongo_config
from utils.load_df_from_file import load_df_from_file
from utils.load_df_from_mongo import load_df_from_mongo
from utils.load_headers import load_headers
from utils.load_spark import load_spark
from utils.rename_cols import rename_cols
from utils.sanitize_df import sanitize_df
from utils.set_cols import set_cols
from utils.upload_df import upload_df
from utils.contributions.convert_to_coords import convert_to_coords
from utils.contributions.filter_out_ineligible_cands import filter_out_ineligible_cands
from utils.contributions.filter_out_zero_amts import filter_out_zero_amts
from utils.contributions.format_df import format_df
from utils.contributions.process_cont_domesticity import process_cont_domesticity

DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year


def process_contributions(
    subject: str,
    file_type: Literal["indiv", "oth", "pas2"],
    file_name: str,
    year: str = None
) -> None:

    print(f"\n{'-' * 100}\n{'-' * 100}")
    print(f"Started processing {subject} Contributions")

    if not year:
        year = decide_year(True)

    output_collection_name = f"{year}_conts"
    uri, db_name = get_mongo_config()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    input_cols = set_cols(
        "cont",
        "input",
        headers,
        file_type
    )

    conts_df = load_df_from_file(
        year,
        file_type,
        file_name,
        spark,
        headers,
        input_cols
    )

    conts_df = filter_out_zero_amts(conts_df)

    conts_df = filter_out_ineligible_cands(
        file_type,
        uri,
        year,
        spark,
        conts_df
    )

    if conts_df is None:
        print("No items to upload, exiting")
        return
    
    conts_df = rename_cols(
        "cont",
        conts_df
    )

    conts_df = format_df(conts_df)

    conts_df = convert_to_coords(
        spark=spark, 
        uri=uri,
        input_df=conts_df
    )

    cands_df = load_df_from_mongo(
        df_type="pandas",
        uri=uri,
        collection_name=f"{year}_cands_raw",
        db_name=db_name,
        fields=[
            "CAND_ID",
            "STATE",
            "DISTRICT",
            "OFFICE"
        ],
        subject="Candidates"
    )

    dists_df = load_df_from_mongo(
        df_type="pandas",
        uri=uri,
        collection_name=f"{year}_dists",
        db_name=db_name,
        fields=[
            "STATE",
            "DISTRICT",
            "GEOMETRY"
        ],
        subject="Districts"
    )

    districtwide_conts_df, statewide_conts_df = process_cont_domesticity(
        cands_df=cands_df,
        dists_df=dists_df,
        conts_df=conts_df.toPandas()
    )

    spark.stop()

    districtwide_conts_df = sanitize_df(
        "cont",
        districtwide_conts_df
    )

    statewide_conts_df = sanitize_df(
        "cont",
        statewide_conts_df
    )

    df = pd.concat(
        objs=[
            districtwide_conts_df,
            statewide_conts_df
        ],
        axis=0
    ).reset_index(drop=True)
    print("\nFinished concatenating Districtwide and Statewide Contributions DataFrames")
    print(f"Item count: {len(df):,}")
    print(df.head())

    df["LOCATION"] = df["LOCATION"].apply(
        lambda x:
            mapping(x) if x is not None else None
    )

    existing_items_df = load_df_from_mongo(
        "pandas",
        uri,
        output_collection_name,
        db_name,
        subject="Existing Items DF"
    )
    if existing_items_df is not None:
        existing_items_cols = set_cols(
            "cont",
            "output",
            cont_type=file_type
        )
        existing_items_cols = [
            col for col in existing_items_cols if col != "LOCATION"
        ]
        df = filter_out_existing_items(
            df,
            existing_items_df,
            existing_items_cols
        )
    if len(df) == 0:
        print("No items to upload, exiting")
        return

    upload_df(
        output_collection_name,
        uri,
        df,
        db_name,
        "append"
    )
    print(df.head())
    
    print(f"\nFinished processing {subject} Contributions")
    print(f"{'-' * 100}\n{'-' * 100}\n")

    return


def process_all_contributions(year: str = None):
    if not year:
        year = decide_year(True)
    process_contributions(
        "Individual",
        "indiv",
        "itcont.txt",
        year
    )
    process_contributions(
        "Committee",
        "pas2",
        "itpas2.txt",
        year
    )
    process_contributions(
        "Other",
        "oth",
        "itoth.txt",
        year
    )


if __name__ == "__main__":
    process_all_contributions()
