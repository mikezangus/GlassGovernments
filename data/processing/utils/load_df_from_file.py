import os
import sys
from pyspark.sql import DataFrame, SparkSession

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.directories import get_raw_file_dir


def load_df_from_file(year: str, file_type: str, file_name: str, spark: SparkSession, headers: list, cols: list) -> DataFrame:
    src_dir = get_raw_file_dir(year, file_type)
    src_path = os.path.join(src_dir, file_name)
    print(f"\nStarted loading DataFrame from file:\n{src_path}")
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    )
    for i, col_name in enumerate(headers):
        df = df.withColumnRenamed(f"_c{i}", col_name)
    df = df.select(*[headers[index] for index in cols])
    print("Finished loading DataFrame")
    print(f"Item count: {df.count():,}")
    df.show()
    return df
