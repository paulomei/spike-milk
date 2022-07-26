#!/usr/bin/env python

import numpy as np
import pickle
import json
import logging
from logging.handlers import TimedRotatingFileHandler 
from flask import Flask, request, jsonify

# Setting a rotating log
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
handler = TimedRotatingFileHandler('./logs/server.log', when = 'midnight', backupCount = 10)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Loading the Flask app with the model
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict_api', methods = ['POST'])

def predict():
    event = json.loads(request.data)
    logging.info('New Request: ' + str(event['values']))
    values = list(map(np.float64, event['values']))
    pre = np.array(values).reshape(1, -1)
    res = model.predict(pre)
    logging.info('Response: ' + str(res[0]))
    return jsonify(res[0])

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
