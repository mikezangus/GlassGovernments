from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when


def filter_df(df: DataFrame, year: str, states: list) -> DataFrame:
    df = df.filter(
        (col("CAND_ELECTION_YR") == year) &
        (col("CAND_STATUS") == "C") &
        (col("CAND_OFFICE") != "P") &
        (col("CAND_OFFICE_ST").isin(states))
    )
    df = df.drop("CAND_STATUS")
    return df
