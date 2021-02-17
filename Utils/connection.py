
import os
import boto3
from dotenv import load_dotenv

load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id', None)
aws_secret_access_key = os.getenv('aws_secret_access_key', None)
bucket_pandas = os.getenv('bucket_pandas', None)
file_name_pandas = os.getenv('file_name_pandas', None)

assert aws_access_key_id
assert aws_secret_access_key
assert bucket_pandas
assert file_name_pandas

def get_file():

    s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    obj = s3.get_object(Bucket= bucket_pandas, Key= file_name_pandas)

    return obj
