import os
import sys
from typing import Literal

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from modules.decide_year import decide_year
from modules.filter_out_existing_items import filter_out_existing_items
from modules.filter_out_zero_amts import filter_out_zero_amts
from modules.get_mongo_uri import get_mongo_uri
from modules.join_dfs import join_dfs
from modules.load_df_from_file import load_df_from_file
from modules.load_df_from_mongo import load_df_from_mongo
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.rename_cols import rename_cont_cols
from modules.sanitize_df import sanitize_df
from modules.set_cols import set_cont_cols
from modules.upload_df import upload_df
from modules.contributions.convert_to_coords import main as convert_to_coords
from modules.contributions.format_df import format_df


def process_contributions(subject: str, file_type: Literal["indiv", "oth", "pas2"], file_name: str, year: str = None) -> None:

    print(f"\n{'-' * 100}\n{'-' * 100}\nStarted processing {subject} Contributions")

    if not year:
        year = decide_year()

    uri = get_mongo_uri()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    input_cols = set_cont_cols("input", file_type, headers)

    main_df = load_df_from_file(year, file_type, file_name, spark, headers, input_cols)

    main_df = filter_out_zero_amts(main_df)
       
    if file_type == "pas2":
        cands_df = load_df_from_mongo(spark, uri, f"{year}_cands", "Candidates", "CAND_ID")
        main_df = join_dfs(main_df, cands_df, "CAND_ID", "inner", "filtering out ineligible candidates")
    else:
        cmtes_df = load_df_from_mongo(spark, uri, f"{year}_cmtes", "Committees", "CAND_ID", "CMTE_ID")
        main_df = join_dfs(main_df, cmtes_df, "CMTE_ID", "inner", "filtering out ineligible candidates")

    if main_df.limit(1).count() == 0:
        print("No items to upload, exiting")
        return
    main_df = rename_cont_cols(main_df)
    main_df = format_df(main_df)
    main_df = convert_to_coords(spark, main_df)
    main_df = sanitize_df(main_df, "cont")

    existing_items_df = load_df_from_mongo(spark, uri, f"{year}_conts", "Existing Items")
    if existing_items_df is not None:
        output_cols = set_cont_cols("output", file_type)
        main_df = filter_out_existing_items(main_df, existing_items_df, output_cols)
    if main_df.limit(1).count() == 0:
        print("No items to upload, exiting")
        return
    
    upload_df(f"{year}_conts", uri, main_df, "append")

    spark.stop()
    
    print(f"\nFinished processing {subject} Contributions\n{'-' * 100}\n{'-' * 100}\n")

    return


def main(year: str = None):
    if not year:
        year = decide_year()
    process_contributions("Individual", "indiv", "itcont.txt", year)
    process_contributions("Committee", "pas2", "itpas2.txt", year)
    process_contributions("Other", "oth", "itoth.txt", year)



if __name__ == "__main__":
    main()
