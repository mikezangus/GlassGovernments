import os
import sys

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from modules.decide_year import decide_year
from modules.get_mongo_uri import get_mongo_uri
from modules.join_dfs import join_dfs
from modules.load_df_from_file import load_df_from_file
from modules.load_df_from_mongo import load_df_from_mongo
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.sanitize_df import sanitize_df
from modules.set_cols import set_cmte_cols
from modules.upload_df import upload_df


def main(year: str = None):

    print(f"\n{'-' * 100}\n{'-' * 100}\nStarted processing Committees")

    file_type = "ccl"

    if not year:
        year = decide_year()

    uri = get_mongo_uri()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    cols = set_cmte_cols("input", headers)
    main_df = load_df_from_file(year, file_type, f"{file_type}.txt", spark, headers, cols)
    cand_df = load_df_from_mongo(spark, uri, f"{year}_cands", "Candidates", "CAND_ID")
    main_df = join_dfs(main_df, cand_df, "CAND_ID", "inner","filter out ineligible candidates")
    main_df = sanitize_df(main_df, "cmte")
    upload_df(f"{year}_cmtes", uri, main_df, "append")

    spark.stop()
    print(f"\nFinished processing Committees\n{'-' * 100}\n{'-' * 100}\n")

    return


if __name__ == "__main__":
    main()
