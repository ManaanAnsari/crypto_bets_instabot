#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:05:07 2021

@author: li
"""

from flask import Flask, request
from flask import jsonify
from make_signals import notify_insta
import json 

# App
app = Flask(__name__)

# Templates
index_template = """
    <h1>Nothing to see here</h1>"""

@app.route("/")
def index():
    return index_template

@app.route('/send_signal/', methods = ['POST'])
def send_signal():
    if request.method == 'POST':
        POST = json.loads(request.data)
        print(POST)
        market, BTCETH = POST.get('market',None), POST.get('BTCETH',None)
        if market and BTCETH:
            if notify_insta(market,BTCETH):
                data = {'message': 'posted successfully'}
                return jsonify(data), 200
            data = {'message': 'Errored out'}
            return jsonify(data), 403
        data = {'message': 'market, BTCETH is missing'}
        return jsonify(data), 406

if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
