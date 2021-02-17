import os
import boto3
from dotenv import load_dotenv

import pymongo
from pymongo import MongoClient

def get_file():
    load_dotenv()
    aws_access_key_id = os.getenv('aws_access_key_id', None)
    aws_secret_access_key = os.getenv('aws_secret_access_key', None)
    bucket_pandas = os.getenv('bucket_pandas', None)
    file_name_pandas = os.getenv('file_name_pandas', None)

    assert aws_access_key_id
    assert aws_secret_access_key
    assert bucket_pandas
    assert file_name_pandas

    s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    obj = s3.get_object(Bucket= bucket_pandas, Key= file_name_pandas)

    return obj

def connect_mongo():
    load_dotenv()
    mongoPass = os.getenv('mongoPass', None)
    mongoUser = os.getenv('mongoUser',None)
    mongoDataBase = os.getenv('mongoDataBase',None)
    mongoCollection = os.getenv('mongoCollection',None)

    assert mongoPass
    assert mongoUser
    assert mongoDataBase
    assert mongoCollection

    cluster = pymongo.MongoClient(f"mongodb+srv://{mongoUser}:{mongoPass}@cluster0.cae74.mongodb.net/{mongoDataBase}?retryWrites=true&w=majority")
    db = cluster[str(mongoDataBase)]
    collection = db[str(mongoCollection)]

    return collection
