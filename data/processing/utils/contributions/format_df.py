from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_format, expr, to_date
from pyspark.sql.types import FloatType


def format_df(input_df: DataFrame) -> DataFrame:
    print("\nStarted formatting Main DataFrame")
    df = input_df \
        .withColumn(
            "AMT",
            input_df["AMT"].cast(FloatType())
        ) \
        .withColumn(
            "ZIP",
            expr("substring(ZIP, 1, 5)")
        ) \
        .withColumn(
            "DATE",
            to_date(
                input_df["DATE"],
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
