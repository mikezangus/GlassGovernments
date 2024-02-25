from pyspark.sql import DataFrame


def rename_cand_cols(df: DataFrame) -> DataFrame:
    df = df \
        .withColumnRenamed("CAND_NAME", "NAME") \
        .withColumnRenamed("CAND_PTY_AFFILIATION", "PARTY") \
        .withColumnRenamed("CAND_ELECTION_YR", "ELECTION_YEAR") \
        .withColumnRenamed("CAND_OFFICE_ST", "STATE") \
        .withColumnRenamed("CAND_OFFICE", "OFFICE") \
        .withColumnRenamed("CAND_OFFICE_DISTRICT", "DISTRICT") \
        .withColumnRenamed("CAND_ICI", "ICI") \
        .withColumnRenamed("CAND_PCC", "CMTE_ID")
    return df


def rename_cont_cols(df: DataFrame) -> DataFrame:
    df = df \
        .withColumnRenamed("ZIP_CODE", "ZIP") \
        .withColumnRenamed("TRANSACTION_AMT", "AMT") \
        .withColumnRenamed("ENTITY_TP", "ENTITY") \
        .withColumnRenamed("TRANSACTION_DT", "DATE")
    return df
