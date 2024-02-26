from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_format, expr, to_date
from pyspark.sql.types import FloatType


def format_df(df: DataFrame) -> DataFrame:
    print("\nStarted formatting Main DataFrame")
    df = df \
        .withColumn(
            "AMT",
            df["AMT"].cast(FloatType())
        ) \
        .withColumn(
            "ZIP",
            expr("substring(ZIP, 1, 5)")
        ) \
        .withColumn(
            "DATE",
            to_date(
                df["DATE"],
                "MMddyyy"
            )
        ) \
        .withColumn(
            "DATE",
            date_format(
                col("DATE"),
                "yyyy-MM-dd"
            )
        )
    print("Finished formatting Main DataFrame")
    print(f"Item count: {(df.count()):,}")
    df.show()
    return df
