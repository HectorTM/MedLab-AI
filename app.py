from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import boto3
import os
from dotenv import load_dotenv
import pandas as pd
import xgboost as xgb

import pymongo
from pymongo import MongoClient

from Utils import connection, calcs, utils
from Model import xgb_model

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
    return jsonify(mean = float(mean), rows = int(rows_number))

@app.route("/amount-prediction",methods=['POST'])
@cross_origin()
def prediction():

    input_data = utils.data_request_to_obj(request)
    
    for key, value in input_data.items():
        if type(value) not in (int,float):
            return  jsonify(success=False, message=f"Error in the input {key} is not numeric")

    collection = connection.connect_mongo()

    DMatrix_input_data = utils.data_to_DMatrix(input_data)
    prediction_value = xgb_model.xgb_prediction(DMatrix_input_data)

    post = {"input_data": input_data, "predictions": prediction_value}
    collection.insert_one(post)

    return jsonify(success=True, result=prediction_value)
