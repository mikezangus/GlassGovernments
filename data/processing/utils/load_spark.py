from pyspark.sql import SparkSession


def load_spark(uri: str) -> SparkSession:
    return SparkSession.builder \
        .appName("SparkProcessing") \
        .master("local[*]") \
        .config(
            "spark.executor.memory",
            "10g"
        ) \
        .config(
            "spark.driver.memory",
            "4g"
        ) \
        .config(
            "spark.default.parallelism",
            10
        ) \
        .config(
            "spark.sql.shuffle.partitions",
            10
        ) \
        .config(
            "spark.driver.extraJavaOptions",
            "-XX:ReservedCodeCacheSize=1g"
        ) \
        .config(
            "spark.executor.extraJavaOptions",
            "-XX:ReservedCodeCacheSize=1g"
        ) \
        .config(
            "spark.jars.packages",
            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
        ) \
        .config(
            "spark.mongodb.input.uri",
            uri
        ) \
        .config(
            "spark.mongodb.output.uri",
            uri
        ) \
        .getOrCreate()
