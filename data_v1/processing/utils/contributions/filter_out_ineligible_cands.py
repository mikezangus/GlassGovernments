import os
import sys
from pyspark.sql import DataFrame, SparkSession

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(UTILS_DIR)
from join_dfs import join_dfs
from load_df_from_mongo import load_df_from_mongo


def filter_out_ineligible_cands(
    file_type: str,
    uri: str,
    year: str,
    spark: SparkSession,
    conts_df: DataFrame
) -> DataFrame | None:
    if file_type == "pas2":
        cands_df = load_df_from_mongo(
            "spark",
            uri,
            f"{year}_cands_raw",
            spark = spark,
            fields = ["CAND_ID"],
            subject = "Candidates"
        )
        df = join_dfs(
            conts_df,
            cands_df,
            "CAND_ID",
            "inner",
            "filtering out ineligible candidates"
        )
    else:
        cmtes_df = load_df_from_mongo(
            "spark",
            uri,
            f"{year}_cmtes",
            spark = spark,
            fields = ["CAND_ID", "CMTE_ID"],
            subject = "Candidates"
        )
        df = join_dfs(
            conts_df,
            cmtes_df,
            "CMTE_ID",
            "inner",
            "filtering out ineligible candidates"
        )

    if df.limit(1).count() == 0:
        return
    return df
