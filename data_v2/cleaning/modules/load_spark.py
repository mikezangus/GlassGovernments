from pyspark.sql import SparkSession, DataFrame as SparkDataFrame


def load_spark(uri: str) -> SparkDataFrame:
    spark = SparkSession.builder \
        .appName("Indiv contributions") \
        .master("local[*]") \
        .config("spark.executor.memory", "10g") \
        .config("spark.driver.memory", "4g") \
        .config("spark.default.parallelism", 10) \
        .config("spark.sql.shuffle.partitions", 10) \
        .config("spark.driver.extraJavaOptions", "-XX:ReservedCodeCacheSize=256M") \
        .config("spark.executor.extraJavaOptions", "-XX:ReservedCodeCacheSize=256M") \
        .config("spark.mongodb.input.uri", uri) \
        .config("spark.mongodb.output.uri", uri) \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()
    return spark
