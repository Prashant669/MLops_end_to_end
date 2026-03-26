import boto3
import sys
from botocore.exceptions import NoCredentialsError


def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"File uploaded successfully to {bucket_name}/{s3_file_path}")
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")


model_path = sys.argv[1]
tfidf_path = sys.argv[2]
local_model_path = s3_model_path = model_path
localtfidf_path = s3_tfidf_path = tfidf_path
s3_bucket_name = 'sentiment-analysis-mlops'

upload_to_s3(local_model_path, s3_bucket_name, s3_model_path)
upload_to_s3(localtfidf_path, s3_bucket_name, s3_tfidf_path)
