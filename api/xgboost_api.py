import joblib 
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)
@app.route('/xgboost_api', methods=['POST']) # Your API endpoint URL would consist /predict

def predict():
	if model:
		try:
			# print(request)
			json_ = request.json
			# print("json: ", json_)
			query = pd.get_dummies(pd.DataFrame(json_))
			query = query.reindex(columns=model_columns, fill_value=0)
			# print("query: ", query)
			prediction_scaled = list(model.predict(query))

			return jsonify({'prediction_scaled': str(prediction_scaled)})

		except:

			return jsonify({'trace': traceback.format_exc()})
	else:
		print ('Train the model first')
		return ('No model here to use')

if __name__ == '__main__':
	try:
		port = int(sys.argv[1]) # This is for a command-line argument
	except:
		port = 12345 # If you don't provide any port then the port will be set to 12345

	model_file_name = 'xgboost_model.pkl'
	model = joblib.load(model_file_name) # Load "xgboost_model.pkl"
	print ('XGBOOST Model loaded')

	model_columns_file_name = 'xgboost_model_columns.pkl'
	model_columns = joblib.load(model_columns_file_name) # Load "xgboost_model_columns.pkl"
	print ('XGBOOST Model columns loaded')

	app.run(port=port, debug=True)