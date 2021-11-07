from pyspark.sql.types import StructField, StructType, StringType, LongType, IntegerType
from pyspark.sql import DataFrameWriter
from pyspark.sql.functions import *
import pyspark

#os.environ['SPARK_HOME'] = '/home/debatosh/spark/spark-3.0.0-bin-hadoop3.2'
from pyspark.sql import SparkSession


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """

spark = SparkSession.builder.appName("SSKafka").getOrCreate()

dsraw = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "192.168.186.100:9092").option(
    "subscribe", "test-output").option("startingOffsets", "earliest").load()

ds = dsraw.selectExpr("CAST(value AS STRING)")

dsraw.printSchema()


custom_schema = StructType([
    StructField("cust_id", StringType(), True),
    StructField("public_ip", StringType(), True),
    StructField("ip", StringType(), True),
    StructField("browser_id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("event_timestamp", StringType(), True),
    StructField("time_spent", StringType(), True),
    StructField("webpage_name", StringType(), True),
    StructField("url", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("country_code", StringType(), True),
    StructField("country_name", StringType(), True),
    StructField("region_name", StringType(), True),
    StructField("city_name", StringType(), True),
    StructField("zip_code", StringType(), True),
    StructField("ip_from", StringType(), True),
])

Person_details_df2 = ds.select(
    from_json(col("value"), custom_schema).alias("Person_details"))

Person_details_df3 = Person_details_df2.select("Person_details.*")

Person_details_df3.printSchema()


db_target_properties = {
    "user": "root", "password": "niit1234", "driver": "com.mysql.jdbc.Driver"}


def foreach_batch_function(df, epoch_id):
    df.write.jdbc(url='jdbc:mysql://192.168.186.100:3306/nginx',
                  table="fact_nginx_log",  properties=db_target_properties, mode="append")
    pass


query = Person_details_df3.writeStream.outputMode(
    "append").foreachBatch(foreach_batch_function).start()

query.awaitTermination()
