# -*-coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import os
#import psycopg2
from bs4 import BeautifulSoup
import requests
import lxml

app = Flask(__name__)
app.secret_key = 'super secret key'

# os.environ['DATABASE_URL'] = 'postgres://'
#
# DATABASE_URL = os.environ['DATABASE_URL']
# print(DATABASE_URL)
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')


data = requests.get("http://www.wylsa.com").text

soup = BeautifulSoup(data, "lxml")


for title in soup.find_all(itemprop='headline'):
    print(title.get_text(), title.parent.get('href'))







if __name__ =='__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(port=5003)
