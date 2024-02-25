import os
import sys

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from modules.decide_year import decide_year
from modules.get_mongo_uri import get_mongo_uri
from modules.load_df_from_file import load_df_from_file
from modules.load_headers import load_headers
from modules.load_spark import load_spark
from modules.rename_cols import rename_cand_cols
from modules.sanitize_df import sanitize_df
from modules.set_cols import set_cand_cols
from modules.upload_df import upload_df
from modules.candidates.load_states import load_states
from modules.candidates.filter_df import filter_df
from modules.candidates.update_districts import update_districts


def main(year: str = None):

    print(f"\n{'-' * 100}\n{'-' * 100}\nStarted processing Candidates")

    file_type = "cn"

    if not year:
        year = decide_year()

    uri = get_mongo_uri()
    spark = load_spark(uri)
    headers = load_headers(file_type)
    cols = set_cand_cols("input", headers)

    df = load_df_from_file(year, file_type, f"{file_type}.txt", spark, headers, cols)
    states = load_states()
    df = filter_df(df, year, states)
    df = rename_cand_cols(df)
    df = update_districts(df)
    df = sanitize_df(df, "cand")
    upload_df(f"{year}_cands", uri, df, "append")

    spark.stop()
    print(f"\nFinished processing Candidates\n{'-' * 100}\n{'-' * 100}\n")

    return


if __name__ == "__main__":
    main()
