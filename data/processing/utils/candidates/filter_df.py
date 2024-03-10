from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def filter_df(input_df: DataFrame, year: str, state_codes: list) -> DataFrame:
    df = input_df.filter(
        (col("CAND_ELECTION_YR") == year) &
        (col("CAND_STATUS") == "C") &
        (col("CAND_OFFICE") != "P") &
        (col("CAND_OFFICE_ST").isin(state_codes))
    )
    df = df.drop("CAND_STATUS")
    return df
