import os
import sys
from pyspark.sql import SparkSession, DataFrame

modules_dir = os.path.dirname(__file__)
processing_dir = os.path.dirname(modules_dir)
data_dir = os.path.dirname(processing_dir)
sys.path.append(data_dir)
from directories import get_src_file_dir


def load_df_from_file(year: str, file_type: str, file_name: str, spark: SparkSession, headers: list, cols: list) -> DataFrame:
    src_dir = get_src_file_dir(year, file_type)
    src_path = os.path.join(src_dir, file_name)
    print(f"\nStarted loading Main DataFrame from file:\n{src_path}")
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    )
    for i, col_name in enumerate(headers):
        df = df.withColumnRenamed(f"_c{i}", col_name)
    df = df.select(*[headers[index] for index in cols])
    print(f"Finished loading Main DataFrame")
    print(f"Item count: {df.count():,}")
    return df
