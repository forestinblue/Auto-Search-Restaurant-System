from flask import Flask, jsonify
import pandas as pd 
class uploadFlask:
    global foodsafetykorea_new_information
    foodsafetykorea_new_information =pd.read_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv')
    global app
    app =  Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    @app.route("/")
    
    def upload_json():
        return jsonify(foodsafetykorea_new_information.to_dict('records'))

