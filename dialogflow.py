#encoding: UTF-8
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

os.environ['DATABASE_URL'] = 'postgres://aszcitgpnlvywd:724a92d4dd1cdb044882cb6f579060b8482e7da45191194cf9b5c7677bc9f210@ec2-54-247-81-88.eu-west-1.compute.amazonaws.com:5432/dfq1utl6uns158'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def remove_bad_characters(list):
    list = [s.replace(',', '') for s in list]
    list = [s.replace(' ', '') for s in list]
    list = [s.replace(':', '') for s in list]
    list = [s.replace(";", '') for s in list]
    list = [s.replace('!', '') for s in list]
    list = [s.replace("'", '') for s in list]
    list = [s.replace("[", '') for s in list]
    list = [s.replace("]", '') for s in list]
    list = [s.replace("{", '') for s in list]
    list = [s.replace("}", '') for s in list]
    list = [s.replace("-", '') for s in list]
    list = [s.replace("_", '') for s in list]
    list = [s.replace("=", '') for s in list]
    list = [s.replace("+", '') for s in list]
    list = [s.replace("|", '') for s in list]
    list = [s.replace("(", '') for s in list]
    list = [s.replace(")", '') for s in list]
    list = [s.replace("*", '') for s in list]
    list = [i for n, i in enumerate(list) if i not in list[n + 1:]] #remove repeating
    print(list)
    return list

#basic response webhook
@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    action = req.get('result').get('action')
    try:
        name = req.get('originalRequest').get('data').get('message').get('chat').get('first_name')
        telegramid = req.get('originalRequest').get('data').get('message').get('chat').get('id')
    except:
        action = 'failed'
        name = 'failed'
        telegramid = 'failed'

    if action == 'starting':
        print('Тебе вітає NewsKit!')
        curs = conn.cursor()
        curs.execute("SELECT * FROM users WHERE telegram_id ='{}' AND name ='{}'".format(telegramid, name))
        user = curs.fetchone()
        if not user:
            curs.execute("INSERT INTO users (telegram_id, name, keywords, send_time, status) VALUES ('{}', '{}', '', '{}', 0)".format(id, name, datetime.now()))
            conn.commit()
        res = {'speech': 'Тебе вітає NewsKit!' + ' Етап реєстрації успішно пройдений!', 'displayText': 'Тебе вітає NewsKit!' + ' Етап реєстрації успішно пройдений!'}
    elif action == 'addkeywords':
        text = req['result']['parameters'].get('keyword')
        if len(text) > 1:
            text = ', '.join(text)
        else:
            text = text[0]
        text = text.lower()
        print(text, 'before0')
        text = text.replace(' і ', ', ')
        text = text.replace(' та ', ', ')
        text = text.replace(' й ', ', ')

        text = text.split(', ')

        curs = conn.cursor()
        curs.execute("SELECT keywords FROM users WHERE telegram_id ='{}' AND name ='{}'".format(telegramid, name))
        try:
            print('user', id, name)
            present_words = curs.fetchone()[0]
        except TypeError:
            present_words = ''
        present_words_list = present_words.split(', ')
        present_words_list = remove_bad_characters(present_words_list)

        text = remove_bad_characters(text)
        print(text)
        #text consists of received list of new keywords

        sendtext = ''

        # loop for detecting repeating keywords
        isgoingtoberemoved = []
        for word in text:
            if word in present_words_list:
                sendtext = sendtext + '\n' + str(word + ' не додано через повтор')
                isgoingtoberemoved.append(word)
            else:
                sendtext = sendtext + '\n' + str(word + ' додано')

        #loop for removing this repeating elements
        for repeated in isgoingtoberemoved:
            text.remove(repeated)


        if len(text) != 0:
            text = ', '.join(text)
        else:
            text = ''.join(text)
        #send_message(present_words_list, chat)
        if len(present_words_list) == 1 and present_words_list[0] == '':
            present_words_list = ''.join(present_words_list)
        else:
            present_words_list = ', '.join(present_words_list)
            if text != '':
                present_words_list = present_words_list + ', '

        if present_words != '':
            present_words = present_words + ', '
        curs.execute("UPDATE users SET keywords ='{}' WHERE telegram_id ='{}' AND name ='{}'".format(str(present_words_list + text), telegramid, name))
        conn.commit()

        sendtext = sendtext + '\n \n' + 'Ваш список ключових слів: ' + str(present_words_list + text)

        res = {'speech': sendtext, 'displayText': sendtext}
    elif action == 'deletekeywords':
        text = req['result']['parameters'].get('keyword')
        if len(text) > 1:
            text = ', '.join(text)
        else:
            text = text[0]
        text = text.lower()
        print(text, 'before0')
        text = text.replace(' і ', ', ')
        text = text.replace(' та ', ', ')
        text = text.replace(' й ', ', ')

        text = text.split(', ')

        sendtext = ''

        curs = conn.cursor()
        curs.execute("SELECT keywords FROM users WHERE telegram_id ='{}' AND name ='{}'".format(telegramid, name))
        present_words = curs.fetchone()[0]
        present_words_list = present_words.split(', ')
        present_words_list = remove_bad_characters(present_words_list)

        #loop for removing chosen elements
        for should_remove in text:
            if should_remove in present_words_list:
                present_words_list.remove(should_remove)
                sendtext = sendtext + '\n' + str(should_remove + ' вилучено')
            else:
                sendtext = sendtext + '\n' + str(should_remove + ' не є твоїм ключовим словом')

        if len(present_words_list) == 1 and present_words_list[0] == '':
            present_words_list = ''.join(present_words_list)
        else:
            present_words_list = ', '.join(present_words_list)

        curs.execute("UPDATE users SET keywords ='{}' WHERE telegram_id ='{}' AND name ='{}'".format(str(present_words_list), telegramid, name))
        conn.commit()

        sendtext = sendtext + '\n \n' + 'Ваш список ключових слів: ' + str(present_words_list)

        res = {'speech': sendtext, 'displayText': sendtext}
    else:
        res = {'speech': 'Сталась помилка', 'displayText': 'Сталась помилка'}
    return make_response(jsonify(res))

@app.route('/', methods=['GET'])
def webhook2():

    res = {'speech': 'Сталась помилка', 'displayText': 'Сталась помилка'}
    return make_response(jsonify(res))




if __name__ == '__main__':
    app.run(debug=True)
