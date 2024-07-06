

from flask import Flask, render_template,jsonify
from pymongo import MongoClient
# from twitter3 import fetch_data
import pandas as pd
import os




# Sentiment_analysis

app = Flask(__name__)

client = MongoClient('')  # Replace with your MongoDB connection string



db = client['web_s']
collection = db['web_s']

@app.route('/get_trends', methods=['GET'])
def get_trends():
    latest_trend = collection.find().sort('_id', -1).limit(1)
    trends_list = ["Not Found"] * 5
    ip_address = "Not Found"
    
    for trend in latest_trend:
        ip_address = trend['ip_address']
        for i in range(min(len(trend['trends']), 5)):
            trends_list[i] = trend['trends'][i]
            
    response = {
        "trends": trends_list,
        "ip_address": ip_address
    }
    
    return jsonify(response)

# @app.route('/fetch_data', methods=['GET'])
# def fetch_data_m():
#     ip_address = fetch_data()
    
#     if ip_address:
#         response = get_trends()
#         data = response.get_json()
#         trends_list = data['trends']
#         ip_address = data['ip_address']

#         print(trends_list,"ip_address:", ip_address)
#         return render_template('index.html', trends=trends_list, ip=ip_address, data=data)
  


@app.route('/')
def index():
    response = get_trends()
    data = response.get_json()
    trends_list = data['trends']
    ip_address = data['ip_address']

    print(trends_list,"ip_address:", ip_address)
    return render_template('index.html', trends=trends_list, ip=ip_address, data=data)

if __name__ == '__main__':
    app.run(debug=True)


