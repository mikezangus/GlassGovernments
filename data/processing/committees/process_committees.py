import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PROCESSING_DIR)
from utils.filter_out_existing_items import filter_out_existing_items
from utils.get_mongo_config import get_mongo_config
from utils.join_dfs import join_dfs
from utils.load_df_from_file import load_df_from_file
from utils.load_df_from_mongo import load_df_from_mongo
from utils.load_headers import load_headers
from utils.load_spark import load_spark
from utils.sanitize_df import sanitize_df
from utils.set_cols import set_cols
from utils.upload_df import upload_df

DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year


def process_committees(year: str = None):
    print(f"\n{'-' * 100}\n{'-' * 100}")
    print("Started processing Committees")
    file_type = "ccl"
    if not year:
        year = decide_year(True)
    output_collection = f"{year}_cmtes"
    uri, _ = get_mongo_config()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    input_cols = set_cols(
        "cmte",
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
    cand_df = load_df_from_mongo(
        "spark",
        uri,
        f"{year}_cands_raw",
        spark=spark,
        fields=["CAND_ID"],
        subject="Candidates"
    )
    main_df = join_dfs(
        main_df,
        cand_df,
        "CAND_ID",
        "inner",
        "filter out ineligible candidates"
    )
    main_df = sanitize_df(
        "cmte",
        main_df
    )
    existing_items_df = load_df_from_mongo(
        "spark",
        uri,
        output_collection,
        spark=spark,
        subject="Existing Items"
    )
    if existing_items_df is not None:
        output_cols = set_cols(
            "cmte",
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
        collection_name=output_collection,
        uri=uri,
        df=main_df,
        mode="append"
    )
    spark.stop()
    print(f"\nFinished processing Committees")
    print(f"{'-' * 100}\n{'-' * 100}\n")
    return


if __name__ == "__main__":
    process_committees()
