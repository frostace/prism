# importing the requests library 
import requests 
import json

# defining the api-endpoint  
API_ENDPOINT = "http://127.0.0.1:12345/predict"

# data to be sent to api 
# data = '[{"adj_close_lag_1":-1.335762949,"adj_close_lag_2":-1.0653761979},"range_hl_lag_1":0.0790925831,"range_hl_lag_2":2.155841619,"range_oc_lag_1":0.5980460874,"range_oc_lag_2":2.2147373628,"volume_lag_1":1.0007798471,"volume_lag_2":1.0859438241,"0_lag1":-1.954737843,"1_lag1":-14.4416495832,"2_lag1":63.646112391,"3_lag1":-10.7318359413,"4_lag1":39.5541503289,"5_lag1":-40.8635897857,"6_lag1":-10.2723266565}]'
# data = [{"Age": 85, "Sex": "male", "Embarked": "S"},{"Age": 24, "Sex": "female", "Embarked": "C"}]

# Opening JSON file 
f = open('../feature_json/test.json',) 

# returns JSON object as a dictionary 
data = json.load(f) 

# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, json = data) 

# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s" % pastebin_url) 