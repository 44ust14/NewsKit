# -*-coding: utf-8 -*-
import json
import urllib
from flask import Flask, jsonify, make_response, request
import requests
import time
from datetime import datetime
import psycopg2
import os
import telepot

app = Flask(__name__)

#basic response webhook
@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    action = req.get('result').get('action')
    if action == 'addkeywords':
        text = req['result']['parameters'].get('keyword')
        print('Окей, додаю ' + text + ' до вашого списку вподобань.')
        res = {'speech': 'Окей, додаю ' + text + ' до вашого списку вподобань.', 'displayText': 'Окей, додаю ' + text + ' до вашого списку вподобань.'}
    elif action == 'starting':
        print('Тебе вітає NewsKit!')
        res = {'speech': 'Тебе вітає NewsKit!', 'displayText': 'Тебе вітає NewsKit!'}
    elif action == 'helping':
        res = {'speech': 'Допомагаю.', 'displayText': 'Допомагаю.'}
    else:
        res = {'speech': 'Сталась помилка', 'displayText': 'Сталась помилка'}
    return make_response(jsonify(res))



if __name__ == '__main__':
    app.run(debug=True)
