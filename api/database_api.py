
# Database Management Service
# TODO: resolve this warning
'''
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
'''

import joblib 
from flask import Flask, request, jsonify, make_response, Response
from flask_restful import Resource, Api
import traceback
import pandas as pd
import numpy as np
from datetime import date
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

app = Flask(__name__)
api = Api(app)

# a DB class to maintain data
class Database():
    def __init__(self):
        self.cur_date = "2019-03-04"
        self.feature = None
        self.real_3d = [1116.050049, 1119.920044, 1140.98999]
        self.pred_new_price = 0
        self.real_pred_90d = [{"date":"2019-02-08","value0":1095.060059,"value1":1097.4630126953},{"date":"2019-02-11","value0":1095.01001,"value1":1085.2906494141},{"date":"2019-02-12","value0":1121.369995,"value1":1104.2950439453},{"date":"2019-02-13","value0":1120.160034,"value1":1121.162109375},{"date":"2019-02-14","value0":1121.670044,"value1":1131.9459228516},{"date":"2019-02-15","value0":1113.650024,"value1":1125.4329833984},{"date":"2019-02-19","value0":1118.560059,"value1":1113.5280761719},{"date":"2019-02-20","value0":1113.800049,"value1":1131.1976318359},{"date":"2019-02-21","value0":1096.969971,"value1":1104.4798583984},{"date":"2019-02-22","value0":1110.369995,"value1":1111.8536376953},{"date":"2019-02-25","value0":1109.400024,"value1":1115.7183837891},{"date":"2019-02-26","value0":1115.130005,"value1":1119.4855957031},{"date":"2019-02-27","value0":1116.050049,"value1":1116.3596191406},{"date":"2019-02-28","value0":1119.920044,"value1":1112.7442626953},{"date":"2019-03-01","value0":1140.98999,"value1":1147.7099609375},{"date":"2019-03-04","value0":1147.800049,"value1":1134.0479736328},{"date":"2019-03-05","value0":1162.030029,"value1":1157.595703125},{"date":"2019-03-06","value0":1157.859985,"value1":1157.0297851562},{"date":"2019-03-07","value0":1143.300049,"value1":1150.6574707031},{"date":"2019-03-08","value0":1142.319946,"value1":1126.8431396484},{"date":"2019-03-11","value0":1175.76001,"value1":1153.7106933594},{"date":"2019-03-12","value0":1193.199951,"value1":1192.6280517578},{"date":"2019-03-13","value0":1193.319946,"value1":1207.703125},{"date":"2019-03-14","value0":1185.550049,"value1":1187.4252929688},{"date":"2019-03-15","value0":1184.459961,"value1":1192.6977539062},{"date":"2019-03-18","value0":1184.26001,"value1":1183.7349853516},{"date":"2019-03-19","value0":1198.849976,"value1":1191.8356933594},{"date":"2019-03-20","value0":1223.969971,"value1":1212.3620605469},{"date":"2019-03-21","value0":1231.540039,"value1":1247.5699462891},{"date":"2019-03-22","value0":1205.5,"value1":1228.4187011719},{"date":"2019-03-25","value0":1193.0,"value1":1197.6314697266},{"date":"2019-03-26","value0":1184.619995,"value1":1199.1218261719},{"date":"2019-03-27","value0":1173.02002,"value1":1181.6552734375},{"date":"2019-03-28","value0":1168.48999,"value1":1161.3210449219},{"date":"2019-03-29","value0":1173.310059,"value1":1149.5017089844},{"date":"2019-04-01","value0":1194.430054,"value1":1174.947265625},{"date":"2019-04-02","value0":1200.48999,"value1":1198.2255859375},{"date":"2019-04-03","value0":1205.920044,"value1":1188.0078125},{"date":"2019-04-04","value0":1215.0,"value1":1206.9193115234},{"date":"2019-04-05","value0":1207.150024,"value1":1210.3623046875},{"date":"2019-04-08","value0":1203.839966,"value1":1206.853515625},{"date":"2019-04-09","value0":1197.25,"value1":1199.84375},{"date":"2019-04-10","value0":1202.160034,"value1":1203.7067871094},{"date":"2019-04-11","value0":1204.619995,"value1":1192.3399658203},{"date":"2019-04-12","value0":1217.869995,"value1":1211.4743652344},{"date":"2019-04-15","value0":1221.099976,"value1":1233.8664550781},{"date":"2019-04-16","value0":1227.130005,"value1":1235.3240966797},{"date":"2019-04-17","value0":1236.339966,"value1":1248.4686279297},{"date":"2019-04-18","value0":1236.369995,"value1":1244.1759033203},{"date":"2019-04-22","value0":1248.839966,"value1":1243.0418701172},{"date":"2019-04-23","value0":1264.550049,"value1":1245.9372558594},{"date":"2019-04-24","value0":1256.0,"value1":1216.9166259766},{"date":"2019-04-25","value0":1263.449951,"value1":1226.5220947266},{"date":"2019-04-26","value0":1272.180054,"value1":1231.3063964844},{"date":"2019-04-29","value0":1287.579956,"value1":1242.1287841797},{"date":"2019-04-30","value0":1188.47998,"value1":1182.7592773438},{"date":"2019-05-01","value0":1168.079956,"value1":1194.5466308594},{"date":"2019-05-02","value0":1162.609985,"value1":1146.4895019531},{"date":"2019-05-03","value0":1185.400024,"value1":1189.28515625},{"date":"2019-05-06","value0":1189.390015,"value1":1192.7280273438},{"date":"2019-05-07","value0":1174.099976,"value1":1195.1062011719},{"date":"2019-05-08","value0":1166.27002,"value1":1169.3858642578},{"date":"2019-05-09","value0":1162.380005,"value1":1154.3283691406},{"date":"2019-05-10","value0":1164.27002,"value1":1165.4924316406},{"date":"2019-05-13","value0":1132.030029,"value1":1137.7735595703},{"date":"2019-05-14","value0":1120.439941,"value1":1117.9997558594},{"date":"2019-05-15","value0":1164.209961,"value1":1160.2333984375},{"date":"2019-05-16","value0":1178.97998,"value1":1176.1049804688},{"date":"2019-05-17","value0":1162.300049,"value1":1179.8422851562},{"date":"2019-05-20","value0":1138.849976,"value1":1132.763671875},{"date":"2019-05-21","value0":1149.630005,"value1":1135.2239990234},{"date":"2019-05-22","value0":1151.420044,"value1":1149.7481689453},{"date":"2019-05-23","value0":1140.77002,"value1":1144.1971435547},{"date":"2019-05-24","value0":1133.469971,"value1":1124.6986083984},{"date":"2019-05-28","value0":1134.150024,"value1":1121.9780273438},{"date":"2019-05-29","value0":1116.459961,"value1":1108.5234375},{"date":"2019-05-30","value0":1117.949951,"value1":1108.9659423828},{"date":"2019-05-31","value0":1103.630005,"value1":1102.9969482422},{"date":"2019-06-03","value0":1036.22998,"value1":1070.2391357422},{"date":"2019-06-04","value0":1053.050049,"value1":1054.6853027344},{"date":"2019-06-05","value0":1042.219971,"value1":1048.0482177734},{"date":"2019-06-06","value0":1044.339966,"value1":1053.3715820312},{"date":"2019-06-07","value0":1066.040039,"value1":1069.7142333984},{"date":"2019-06-10","value0":1080.380005,"value1":1076.7004394531},{"date":"2019-06-11","value0":1078.719971,"value1":1074.3411865234},{"date":"2019-06-12","value0":1077.030029,"value1":1071.7741699219},{"date":"2019-06-13","value0":1088.77002,"value1":1084.8933105469},{"date":"2019-06-14","value0":1085.349976,"value1":1083.7854003906},{"date":"2019-06-17","value0":1092.5,"value1":1085.8825683594},{"date":"2019-06-18","value0":1103.599976,"value1":1093.8271484375}]

db = Database()

def update_real_3d(real_3d, new_price):
    """@params:
        real_3d: List[int]
        new_price: int 
    """
    # left shift the real_3d for 1 day
    return real_3d[1:] + [new_price]

def update_real_pred_90d(real_pred_90d, real_new_price_w_date=None, pred_new_price_w_date=None):
    """@params:
        real_pred_90d: List[dict]
        real_new_price_w_date: dict: {"date": , "value": } 
        pred_new_price_w_date: dict: {"date": , "value": } 
        one of real_new_price_w_date and pred_new_price_w_date must be None
    """
    # take care of the parallelism of real and pred price
    last_day_price = real_pred_90d[-1]
    if not last_day_price["value0"] or not last_day_price["value1"]:
        # one of them is None, only update one entry
        real_pred_90d[-1]["value0"], real_pred_90d[-1]["value1"] = real_new_price_w_date["value"] if real_new_price_w_date else last_day_price["value0"], pred_new_price_w_date["value"] if pred_new_price_w_date else last_day_price["value1"]
    else:
        # left shift and update one entry
        date = (real_new_price_w_date or pred_new_price_w_date)["date"]
        real_pred_90d = real_pred_90d[1:] + [{"date": date, "value0": real_new_price_w_date["value"] if real_new_price_w_date else None, "value1": pred_new_price_w_date["value"] if pred_new_price_w_date else None}]
    return real_pred_90d

# implement a DBMS class
class DBMS(Resource):
    def get(self, data_name):
        global db
        # options:
        #   - feature
        #   - real_3d
        #   - real_pred_90d
        try:
            print("request for " + data_name + " received", end=": ")
            if data_name == 'feature':
                print(db.feature)
                return db.feature
            elif data_name == "real_3d":
                print(db.real_3d)
                return db.real_3d
            elif data_name == "real_pred_90d":
                print(db.real_pred_90d)
                return db.real_pred_90d
            else:
                print("data name not found!")
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})

    def post(self, data_name):
        global db
        # options:
        #   - feature
        #   - real_new_price (used to update real_3d and real_pred_90d)
        #   - pred_new_price
        try:
            if data_name == 'feature':
                db.feature = request.json
            elif data_name == "real_new_price":
                real_new_price_with_date = request.json
                real_new_date = real_new_price_with_date["date"]
                if date.fromisoformat(db.cur_date) >= date.fromisoformat(real_new_date): return "Duplicate Date"
                real_new_price = real_new_price_with_date["value"]
                # real_new_price_with_date["value"] = real_new_price
                db.cur_date = real_new_date
                db.real_3d = update_real_3d(db.real_3d, real_new_price)
                db.real_pred_90d = update_real_pred_90d(db.real_pred_90d, real_new_price_with_date, None)
            elif data_name == "pred_new_price":
                pred_new_price_with_date = request.json
                pred_new_date = pred_new_price_with_date["date"]
                if date.fromisoformat(db.cur_date) >= date.fromisoformat(pred_new_date): return "Duplicate Date"
                pred_new_price = pred_new_price_with_date["value"]
                # pred_new_price_with_date["value"] = pred_new_price
                db.pred_new_price = pred_new_price
                db.real_pred_90d = update_real_pred_90d(db.real_pred_90d, None, pred_new_price_with_date)
            else:
                print("data name not found!")
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})
        print(data_name + " updated: ", request.json)
        # print(db.real_pred_90d)
        return "RCV"

    def options(self, data_name):
        resp = Response("Test CORS")
        resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        resp.headers['Access-Control-Allow-Methods'] = 'GET'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

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