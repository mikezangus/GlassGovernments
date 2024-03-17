import os
import sys

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
from utils.candidates.filter_df import filter_df
from utils.candidates.update_districts import update_districts
DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year
from geography.usa.states.load_states import load_states


def process_candidates(year: str = None):
    print(f"\n{'-' * 100}\n{'-' * 100}")
    print("Started processing Candidates")
    file_type = "cn"
    if not year:
        year = decide_year(True)
    output_collection = f"{year}_cands_raw"
    uri, _ = get_mongo_config()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    input_cols = set_cols(
        "cand",
        "input",
        headers
    )
    main_df = load_df_from_file(
        year,
        file_type,
        f"{file_type}.txt",
        spark,
        headers,
        input_cols
    )
    state_codes = load_states(
        "all",
        "code_list"
    )
    main_df = filter_df(
        main_df,
        year,
        state_codes
    )
    main_df = rename_cols(
        "cand",
        main_df
    )
    main_df = update_districts(main_df)
    main_df = sanitize_df(
        "cand",
        main_df
    )
    existing_items_df = load_df_from_mongo(
        "spark",
        uri,
        output_collection,
        spark = spark
    )
    if existing_items_df is not None:
        output_cols = set_cols(
            "cand",
            "output"
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
        "overwrite"
    )
    spark.stop()
    print(f"\nFinished processing Candidates")
    print(f"{'-' * 100}\n{'-' * 100}\n")
    return


if __name__ == "__main__":
    process_candidates()
