from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when


def update_districts(df: DataFrame) -> DataFrame:
    df = df \
        .withColumn(
            "DISTRICT",
            when(
                col("OFFICE") != "H",
                col("OFFICE")
            ) \
            .otherwise(col("DISTRICT")))
    return df
