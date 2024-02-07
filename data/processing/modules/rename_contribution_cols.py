from pyspark.sql import DataFrame


def rename_cols(df: DataFrame) -> DataFrame:
    df = df \
        .withColumnRenamed("ENTITY_TP", "ENTITY") \
        .withColumnRenamed("ZIP_CODE", "ZIP") \
        .withColumnRenamed("TRANSACTION_DT", "TRAN_DATE") \
        .withColumnRenamed("TRANSACTION_AMT", "TRAN_AMT")
    return df