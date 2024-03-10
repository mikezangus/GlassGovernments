import os
import sys
from typing import Literal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PROCESSING_DIR)
from utils.filter_out_existing_items import filter_out_existing_items
from utils.get_mongo_config import get_mongo_config
from utils.join_dfs import join_dfs
from utils.load_df_from_file import load_df_from_file
from utils.load_df_from_mongo import load_spark_df_from_mongo
from utils.load_headers import load_headers
from utils.load_spark import load_spark
from utils.rename_cols import rename_cols
from utils.sanitize_df import sanitize_df
from utils.set_cols import set_cols
from utils.upload_df import upload_df
from utils.contributions.convert_to_coords import convert_to_coords
from utils.contributions.filter_out_zero_amts import filter_out_zero_amts
from utils.contributions.format_df import format_df

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

    output_collection = f"{year}_conts"
    uri, _ = get_mongo_config()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    input_cols = set_cols(
        "cont",
        "input",
        headers,
        file_type
    )

    main_df = load_df_from_file(
        year,
        file_type,
        file_name,
        spark,
        headers,
        input_cols
    )

    main_df = filter_out_zero_amts(main_df)
       
    if file_type == "pas2":
        cands_df = load_spark_df_from_mongo(
            spark,
            uri,
            f"{year}_cands",
            ["CAND_ID"],
            "Candidates"
        )
        main_df = join_dfs(
            main_df,
            cands_df,
            "CAND_ID",
            "inner",
            "filtering out ineligible candidates"
        )
    else:
        cmtes_df = load_spark_df_from_mongo(
            spark,
            uri,
            f"{year}_cmtes",
            ["CAND_ID", "CMTE_ID"],
            "Candidates"
        )
        main_df = join_dfs(
            main_df,
            cmtes_df,
            "CMTE_ID",
            "inner",
            "filtering out ineligible candidates"
        )

    if main_df.limit(1).count() == 0:
        print("No items to upload, exiting")
        return
    main_df = rename_cols(
        "cont",
        main_df
    )
    main_df = format_df(main_df)
    main_df = convert_to_coords(
        spark, 
        uri,
        main_df
    )
    main_df = sanitize_df(
        "cont",
        main_df
    )
    existing_items_df = load_spark_df_from_mongo(
        spark,
        uri,
        output_collection,
        subject = "Existing Items"
    )
    if existing_items_df is not None:
        output_cols = set_cols(
            "cont",
            "output",
            cont_type = file_type
        )
        main_df = filter_out_existing_items(
            main_df,
            existing_items_df,
            output_cols
        )
    if main_df.limit(1).count() == 0:
        print("No items to upload, exiting")
        return

    upload_df(
        output_collection,
        uri,
        main_df,
        "append"
    )

    spark.stop()
    
    print(f"\nFinished processing {subject} Contributions")
    print(f"{'-' * 100}\n{'-' * 100}\n")

    return


def main(year: str = None):
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
    main()
