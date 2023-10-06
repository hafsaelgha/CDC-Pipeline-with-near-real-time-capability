import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql import DataFrame, Row
import datetime
from awsglue import DynamicFrame
import gs_flatten
from awsglueml.transforms import EntityDetector
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import *

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon Kinesis
dataframe_AmazonKinesis_node1696620835179 = glueContext.create_data_frame.from_options(
    connection_type="kinesis",
    connection_options={
        "typeOfData": "kinesis",
        "streamARN": "arn:aws:kinesis:us-east-1:365071006849:stream/kinesis-aurora",
        "classification": "json",
        "startingPosition": "earliest",
        "inferSchema": "true",
    },
    transformation_ctx="dataframe_AmazonKinesis_node1696620835179",
)


def processBatch(data_frame, batchId):
    if data_frame.count() > 0:
        AmazonKinesis_node1696620835179 = DynamicFrame.fromDF(
            glueContext.add_ingestion_time_columns(data_frame, "hour"),
            glueContext,
            "from_data_frame",
        )
        # Script generated for node Flatten
        Flatten_node1696620925904 = AmazonKinesis_node1696620835179.gs_flatten(
            maxLevels=0
        )

        # Script generated for node Detect Sensitive Data
        entity_detector = EntityDetector()
        classified_map = entity_detector.classify_columns(
            Flatten_node1696620925904, ["PHONE_NUMBER", "EMAIL"], 1.0, 0.1
        )

        def maskDf(df, keys):
            if not keys:
                return df
            df_to_mask = df.toDF()
            for key in keys:
                df_to_mask = df_to_mask.withColumn(key, lit("########"))
            return DynamicFrame.fromDF(df_to_mask, glueContext, "updated_masked_df")

        DetectSensitiveData_node1696621004664 = maskDf(
            Flatten_node1696620925904, list(classified_map.keys())
        )

        # Script generated for node Amazon S3
        AmazonS3_node1696621151060_path = "s3://aurora-kinesis-demo/data-output/"
        AmazonS3_node1696621151060 = glueContext.getSink(
            path=AmazonS3_node1696621151060_path,
            connection_type="s3",
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=["ingest_year", "ingest_month", "ingest_day", "ingest_hour"],
            compression="snappy",
            enableUpdateCatalog=True,
            transformation_ctx="AmazonS3_node1696621151060",
        )
        AmazonS3_node1696621151060.setCatalogInfo(
            catalogDatabase="default", catalogTableName="kinesis-users"
        )
        AmazonS3_node1696621151060.setFormat("glueparquet")
        AmazonS3_node1696621151060.writeFrame(DetectSensitiveData_node1696621004664)


glueContext.forEachBatch(
    frame=dataframe_AmazonKinesis_node1696620835179,
    batch_function=processBatch,
    options={
        "windowSize": "60 seconds",
        "checkpointLocation": args["TempDir"] + "/" + args["JOB_NAME"] + "/checkpoint/",
    },
)
job.commit()
