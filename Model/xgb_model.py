
import os
import xgboost as xgb

def xgb_prediction(DMatrix_data):
    
    assert os.path.exists('../my_model.model')
    loaded_model = xgb.Booster()
    loaded_model.load_model('../my_model.model')
    prediction_value = float(loaded_model.predict(DMatrix_data)[0])

    return prediction_value