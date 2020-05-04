# importing the requests library 
import requests 
import json
import numpy as np
import ast

# defining the api-endpoint  
XGBOOST_API_ENDPOINT = "http://127.0.0.1:12345/xgboost_api"
DATABASE_API_ENDPOINT = "http://127.0.0.1:12346/database_api"

# e.g. : feature = [{"adj_close_lag_1":-1.335762949,"adj_close_lag_2":-1.0653761979},"range_hl_lag_1":0.0790925831,"range_hl_lag_2":2.155841619,"range_oc_lag_1":0.5980460874,"range_oc_lag_2":2.2147373628,"volume_lag_1":1.0007798471,"volume_lag_2":1.0859438241,"0_lag1":-1.954737843,"1_lag1":-14.4416495832,"2_lag1":63.646112391,"3_lag1":-10.7318359413,"4_lag1":39.5541503289,"5_lag1":-40.8635897857,"6_lag1":-10.2723266565}]

# TODO: wrap up the following inside a function
### ====== Load model and predict ==============================
# Opening feature JSON file 
f = open('../json/test.json',) 

# returns JSON object as a dictionary 
feature = json.load(f) 

# sending post request and saving response as response object 
xgb_response = requests.post(url = XGBOOST_API_ENDPOINT, json = feature) 

# extracting response text: scaled prediction
# convert stringified json to listed json for scaled_prediction
result_json = json.loads(xgb_response.text)                 # json obj          e.g.: {'prediction_scaled': '[-1.4321082]'}
predicted_value_json = result_json['prediction_scaled']     # string of a list  e.g.: '[-1.4321082]'
prediction_scaled = json.loads(predicted_value_json)        # list              e.g.: [-1.4321082]
print("The scaled prediction is:%s" % prediction_scaled) 
### ===========================================================

### ====== reverse scale mapping ==============================
# get real_3d from database_api
db_response = requests.get(url = DATABASE_API_ENDPOINT + "/real_3d") 
price_str = db_response.text
prev_N_price = ast.literal_eval(price_str)

'''price_file = open('../json/prev_N_price.json',) 
prev_N_price = json.load(price_file) # loads function support str -> list
prev_N_price = json.loads(prev_N_price)'''

# compute std and mean
adj_price_mean, adj_price_std = np.mean(prev_N_price), np.std(prev_N_price)

# reverse scale mapping function
def reverse_scale(prediction_scaled):
    global adj_price_std, adj_price_mean
    prediction = prediction_scaled * adj_price_std + adj_price_mean
    return prediction

# mapping
prediction = list(map(reverse_scale, prediction_scaled))

# TODO: post predicted price to database_api/pred_tmr_price: {"date": , "value": }
print("The original prediction is:%s" % prediction) 
### ===========================================================