
import pandas as pd
import xgboost as xgb

def data_to_DMatrix(data):
    df_input_data= pd.DataFrame([data])
    Dmatrix_input_data = xgb.DMatrix(df_input_data)

    return Dmatrix_input_data

def data_request_to_obj(request):

    data = request.get_json()
    #DMatrix(1,6) [weekend	passenger_count	trip_distance	RatecodeID	payment_type	tip_amount]
    weekend = data["weekend"]
    passenger_count = data["passenger_count"]	
    trip_distance = data["trip_distance"]	
    RatecodeID = data["RatecodeID"]	
    payment_type = data["payment_type"]	
    tip_amount = data["tip_amount"]

    input_data = {"weekend":weekend, "passenger_count":passenger_count, "trip_distance":trip_distance,"RatecodeID":RatecodeID,"payment_type":payment_type,"tip_amount":tip_amount}

    return input_data