# importing the requests library 
import requests 
import json
import numpy as np
import ast
from datetime import date

# defining the api-endpoint  
XGBOOST_API_ENDPOINT = "http://127.0.0.1:12345/xgboost_api"
DATABASE_API_ENDPOINT = "http://127.0.0.1:12346/database_api"

# e.g. : data = {"date": "2019-03-04", "feature": {"adj_close_lag_1":{"0":-1.335762949},"adj_close_lag_2":{"0":-1.0653761979}...}}

# TODO: wrap up the following inside a function
### ====== Load model and predict ==============================
# Opening feature JSON file 
f = open('../json/test.json',) 

# returns JSON object as a dictionary 
data = json.load(f)
cur_date = data["date"]
feature = data["feature"]

# sending post request and saving response as response object 
xgb_response = requests.post(url = XGBOOST_API_ENDPOINT, json = feature) 

# extracting response text: scaled prediction
# convert stringified json to listed json for scaled_prediction
result_json = json.loads(xgb_response.text)                 # json obj          e.g.: {'prediction_scaled': '[-1.4321082]'}
predicted_value_json = result_json['prediction_scaled']     # string of a list  e.g.: '[-1.4321082]'
prediction_scaled = json.loads(predicted_value_json)        # list              e.g.: [-1.4321082]
print("The scaled prediction is:%s" % prediction_scaled[0]) 
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
prediction = list(map(reverse_scale, prediction_scaled))[0]

# post predicted price to database_api/pred_new_price: {"date": , "value": }
print("The original prediction is:%s" % prediction)
pred_new_price = {"date": cur_date, "value": prediction}
database_response = requests.post(url = DATABASE_API_ENDPOINT + "/pred_new_price", json = pred_new_price) 
print(database_response.text)
# TODO: add 3 way handshake to make comm more stable
### ===========================================================