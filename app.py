from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import boto3
import os
from dotenv import load_dotenv
import pandas as pd
import xgboost as xgb

import pymongo
from pymongo import MongoClient

from Utils import connection, calcs

app = Flask(__name__)


@app.route("/")
def intro():
    return "The valid endpoints are: '/mean-tips' and 'amount-prediction'"

@app.route("/mean-tips")
@cross_origin()
def mean_tips():
    obj = connection.get_file()
    df = calcs.streamBody_to_CSV_tips(obj)
    mean = calcs.mean_pandas(df)
    rows_number = calcs.rows_number(df)

    # print("mean {mean:.2f}, rows {rows}".format(mean = mean, rows = rows_number))
    # {"mean":1.750663115812088,"rows":10906858}
    return jsonify(mean = float(mean), rows = int(rows_number))

@app.route("/amount-prediction",methods=['POST'])
@cross_origin()
def prediction():

    data = request.get_json()
    #DMatrix(1,6) [weekend	passenger_count	trip_distance	RatecodeID	payment_type	tip_amount]
    weekend = data["weekend"]
    passenger_count = data["passenger_count"]	
    trip_distance = data["trip_distance"]	
    RatecodeID = data["RatecodeID"]	
    payment_type = data["payment_type"]	
    tip_amount = data["tip_amount"]

    input_data = {"weekend":weekend, "passenger_count":passenger_count, "trip_distance":trip_distance,"RatecodeID":RatecodeID,"payment_type":payment_type,"tip_amount":tip_amount}
    
    for key, value in input_data.items():
        if type(value) not in (int,float):
            return  jsonify(success=False, message=f"Error in the input {key} is not numeric")

    df_input_data= pd.DataFrame([input_data])
    Dmatrix_input_data = xgb.DMatrix(df_input_data)

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

    assert os.path.exists('../my_model.model')

    loaded_model = xgb.Booster()
    loaded_model.load_model('../my_model.model')

    # And use it for predictions.
    prediction_value = float(loaded_model.predict(Dmatrix_input_data)[0])

    post = {"input_data": input_data, "predictions": prediction_value}
    collection.insert_one(post)

    return jsonify(success=True, result=prediction_value)


# @app.route("/getData")
# def gat_data_from_aws():
#     bucket = "----"
#     file_name = "----"
#     aws_access_key_id='----'
#     aws_secret_access_key='----'

#     s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

#     with open('mmg_data.csv', 'wb') as f:
#         s3.download_fileobj(bucket, file_name, f)

#     # # get object and file (key) from bucket
#     # obj = s3.get_object(Bucket= bucket, Key= file_name) 
#     # df = pd.read_csv(obj['Body']) # 'Body' is a key word from the dict

#     print(os.getcwd()) #to control where we are at the moment
#     # df.to_csv('C:\Users\PC_Hector\Documents\MedLab\MedLabData.csv', index = False, header = True)

#     return "pistacho"
 

@app.route("/test")
def test():
    number = 12.35465

    print(os.getcwd())
    assert os.path.exists('../my_model.model')

    df1 = pd.DataFrame([(1,2,None),(None,4,None),(5,None,7),(5,None,None)], 
                        columns=['a','b','d'], index = ['A', 'B','C','D'])
    print(df1.count())
    print(df1["a"].count())
    
    load_dotenv()
    SECRET_KEY = os.getenv('aws_access_key_id', None)
    assert SECRET_KEY
    print(SECRET_KEY)
    
    return f"number {number:.2f}"

@app.route("/connectiontest")
def test_mongo():
    load_dotenv()
    mongoPass = os.getenv('mongoPass', None)
    mongoUser = os.getenv('mongoUser',None)
    mongoDataBase = os.getenv('mongoDataBase',None)
    mongoCollection = os.getenv('mongoCollection',None)

    assert mongoPass
    assert mongoUser
    assert mongoDataBase
    assert mongoCollection

    cluster = pymongo.MongoClient("mongodb+srv://{mongoUser}:{mongoPass}@cluster0.cae74.mongodb.net/{mongoDataBase}?retryWrites=true&w=majority".format(
        mongoUser = mongoUser, mongoPass = mongoPass , mongoDataBase = mongoDataBase
    ))
    db = cluster[str(mongoDataBase)]
    collection = db[str(mongoCollection)]

    post = {"name": "test", "score":123}
    collection.insert_one(post)

    return ''