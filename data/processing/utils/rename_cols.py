from pyspark.sql import DataFrame
from typing import Literal


def rename_cols(type: Literal["cand", "cont"], input_df: DataFrame) -> DataFrame:
    if type == "cand":
        df = input_df \
            .withColumnRenamed("CAND_NAME", "FEC_NAME") \
            .withColumnRenamed("CAND_PTY_AFFILIATION", "PARTY") \
            .withColumnRenamed("CAND_ELECTION_YR", "YEAR") \
            .withColumnRenamed("CAND_OFFICE_ST", "STATE") \
            .withColumnRenamed("CAND_OFFICE", "OFFICE") \
            .withColumnRenamed("CAND_OFFICE_DISTRICT", "DISTRICT") \
            .withColumnRenamed("CAND_ICI", "ICI")
    elif type == "cont":
        df = input_df \
            .withColumnRenamed("ZIP_CODE", "ZIP") \
            .withColumnRenamed("TRANSACTION_AMT", "AMT") \
            .withColumnRenamed("ENTITY_TP", "ENTITY") \
            .withColumnRenamed("TRANSACTION_DT", "DATE")
    return df
