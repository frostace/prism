
# Database Management Service
'''
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
'''

import joblib 
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)

# a DB class to maintain data
class Database():
    def __init__(self):
        self.cur_date = "2019-03-04"
        self.feature = None
        self.real_3d = [1116.050049, 1119.920044, 1140.98999]
        self.pred_tmr_price = 0
        self.real_pred_15d = [{"date":"2019-02-08","value0":1095.060059,"value1":1097.463},{"date":"2019-02-11","value0":1095.01001,"value1":1085.2906},{"date":"2019-02-12","value0":1121.369995,"value1":1104.295},{"date":"2019-02-13","value0":1120.160034,"value1":1121.1621},{"date":"2019-02-14","value0":1121.670044,"value1":1131.9459},{"date":"2019-02-15","value0":1113.650024,"value1":1125.433},{"date":"2019-02-19","value0":1118.560059,"value1":1113.5281},{"date":"2019-02-20","value0":1113.800049,"value1":1131.1976},{"date":"2019-02-21","value0":1096.969971,"value1":1104.4799},{"date":"2019-02-22","value0":1110.369995,"value1":1111.8536},{"date":"2019-02-25","value0":1109.400024,"value1":1115.7184},{"date":"2019-02-26","value0":1115.130005,"value1":1119.4856},{"date":"2019-02-27","value0":1116.050049,"value1":1116.3596},{"date":"2019-02-28","value0":1119.920044,"value1":1112.7443},{"date":"2019-03-01","value0":1140.98999,"value1":1147.71}]

db = Database()

def update_real_3d(real_3d, new_price):
    """@params:
        real_3d: List[int]
        new_price: int 
    """
    # left shift the real_3d for 1 day
    return real_3d[1:] + [new_price]

def update_real_pred_15d(real_pred_15d, real_new_price=None, pred_new_price=None):
    """@params:
        real_pred_15d: List[dict]
        real_new_price: dict: {"date": , "value": } 
        pred_new_price: dict: {"date": , "value": } 
        one of real_new_price and pred_new_price must be None
    """
    # take care of the parallelism of real and pred price
    last_day_price = real_pred_15d[-1]
    if not last_day_price["value0"] or not last_day_price["value1"]:
        # one of them is None, only update one entry
        real_pred_15d[-1]["value0"], real_pred_15d[-1]["value1"] = real_new_price if real_new_price else last_day_price["value0"], pred_new_price if pred_new_price else last_day_price["value1"]
    else:
        # left shift and update one entry
        date = (real_new_price or pred_new_price)["date"]
        real_pred_15d = real_pred_15d[1:] + [{"date": date, "value0":real_new_price, "value1": pred_new_price}]

# implement a DBMS class
class DBMS(Resource):
    def get(self, data_name):
        global db
        # options:
        #   - feature
        #   - real_3d
        #   - real_pred_15d
        try:
            print("request for " + data_name + " received")
            if data_name == 'feature':
                print(db.feature)
                return db.feature
            elif data_name == "real_3d":
                print(db.real_3d)
                return db.real_3d
            elif data_name == "real_pred_15d":
                print(db.real_pred_15d)
                return db.real_pred_15d
            else:
                print("data name not found!")
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})

    def post(self, data_name):
        global db
        # options:
        #   - feature
        #   - real_new_price (used to update real_3d and real_pred_15d)
        #   - pred_tmr_price
        try:
            if data_name == 'feature':
                db.feature = request.json
            elif data_name == "real_new_price":
                new_date = request.json["date"]
                new_price = request.json["value"]
                db.cur_date = new_date
                db.real_3d = update_real_3d(db.real_3d, new_price)
                db.real_pred_15d = update_real_pred_15d(db.real_pred_15d, new_price)
            elif data_name == "pred_tmr_price":
                pred_new_date = request.json["date"]
                pred_new_price = request.json["value"]
                db.pred_tmr_price = pred_new_price
                db.real_pred_15d = update_real_pred_15d(db.real_pred_15d, pred_new_price)
            else:
                print("data name not found!")
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})
        print(data_name + " updated: ", request.json)

# @app.route('/database_api', methods=['POST']) # Your API endpoint URL would consist /predict
# def newhome():
#     print(request.json)
#     return "test" 

# @app.route('/database_api', methods=['GET']) # Your API endpoint URL would consist /predict
# def home():
#     return "test"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(DBMS, '/database_api/<data_name>', endpoint="database_api")

if __name__ == '__main__':
	try:
		port = int(sys.argv[1]) # This is for a command-line argument
	except:
		port = 12346 # If you don't provide any port then the port will be set to 12345

	print ('Database Management Running...')

	app.run(port=port, debug=True)