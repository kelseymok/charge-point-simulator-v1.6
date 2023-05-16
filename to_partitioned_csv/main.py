import glob
import shutil
from typing import Dict, List
import os


import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import year, month, dayofmonth, col, to_timestamp, concat, hour, minute, lpad

basename = "1680355141"


def partition():
    spark = SparkSession.builder.appName("gold").getOrCreate()
    df = spark.read.options(header='True', inferSchema='True', delimiter=',') \
      .csv(f"../out/{basename}.csv.gz")


    def write(input_df: DataFrame) -> None:
        input_df.write.option("header", True). \
            partitionBy("partition_col"). \
            mode("overwrite"). \
            csv(f"./output/{basename}-original/")

    def create_partition_column(input_df: DataFrame) -> DataFrame:
        return input_df.withColumn("write_timestamp_new", to_timestamp(col("write_timestamp"))). \
            withColumn("year", year(col("write_timestamp"))).\
            withColumn("month", month(col("write_timestamp"))).\
            withColumn("day", dayofmonth(col("write_timestamp"))).\
            withColumn("hour", hour(col("write_timestamp"))).\
            withColumn("minute", minute(col("write_timestamp"))).\
            withColumn("partition_col", concat(
            col("year"),
            lpad(col("month"), 2, "0"),
            lpad(col("day"), 2, "0"),
            lpad(col("hour"), 2, "0"),
            lpad(col("minute"), 2, "0"))).\
            where("month = 1"). \
            where("day <= 5"). \
            drop("write_timestamp_new").\
            drop("year").\
            drop("month").\
            drop("day").\
            drop("hour").\
            drop("minute")

    df_partitioned = df.transform(create_partition_column)
    df_partitioned.printSchema()
    df_partitioned.show()
    write(df_partitioned)


# partition()

# File source - Reads files written in a directory as a stream of data. Files will be processed in the order of file modification time. If latestFirst is set, order will be reversed. Supported file formats are text, CSV, JSON, ORC, Parquet. See the docs of the DataStreamReader interface for a more up-to-date list, and supported options for each file format. Note that the files must be atomically placed in the given directory, which in most file systems, can be achieved by file move operations.





def extract_meta(path: str) -> Dict:
    parts = path.split("/")
    _, partition_col = parts[3].split("=")
    return {"path": path, "partition_col": partition_col}


def sort(files: List) -> pd.DataFrame:
    metadata_df = pd.DataFrame([ extract_meta(f) for f in files ])
    metadata_df.sort_values(["partition_col"], inplace=True)
    return metadata_df

def rename_files(input_df: pd.DataFrame, new_dir: str):
    records = input_df.to_dict(orient="records")
    for f in records:
        new_name = f"{new_dir}/{f['partition_col']}.csv"
        print(f"renaming {f['path']} to {new_name}")
        os.rename(f['path'], new_name)

def cleanup(original_dir: str):
    shutil.rmtree(original_dir)


partition()

paths = glob.glob(f"./output/" + '/**/*.csv', recursive=True)
new_dir = f"./output/{basename}"
if not os.path.exists(new_dir):
    os.mkdir(new_dir)

rename_files(sort(paths), new_dir=new_dir)
shutil.make_archive(f"./output/{basename}", 'zip', new_dir)

cleanup(f"./output/{basename}-original/")
cleanup(f"./output/{basename}/")
