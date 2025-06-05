import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Load from RDS
datasource = glueContext.create_dynamic_frame.from_catalog(database="rds-db", table_name="customer")

# Transformation logic
transformed = ApplyMapping.apply(frame=datasource, mappings=[
    ("customer_id", "int", "customer_id", "int"),
    ("name", "string", "full_name", "string"),
    ("email", "string", "email_address", "string")
])

# Write to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=transformed,
    catalog_connection="redshift-connection",
    connection_options={"dbtable": "public.customer", "database": "dw"},
    redshift_tmp_dir="s3://your-temp-dir/"
)
