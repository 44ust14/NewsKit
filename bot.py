import json
import requests
import time
from datetime import datetime
import urllib
import psycopg2
import os

os.environ['DATABASE_URL'] = 'postgres://aszcitgpnlvywd:724a92d4dd1cdb044882cb6f579060b8482e7da45191194cf9b5c7677bc9f210@ec2-54-247-81-88.eu-west-1.compute.amazonaws.com:5432/dfq1utl6uns158'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')



TOKEN = '582815834:AAFkPhSrT-yfSq0Vi6dI8bMTFXovoVWT0Ok'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]

        id = update['message']['chat']['id']
        name =  update['message']['chat']['first_name']

        if text == '/start':
            text = 'Тебе вітає Newkit! Повідом мені свої ключові слова таким чином: \nКлючові слова: слово1, слово2, слово3 і тд \n або \n/keywords слово1, слово2, слово3'
            send_message(text, chat)

            text = str([update['message']['chat']['id'], update['message']['chat']['first_name']])
            curs = conn.cursor()
            curs.execute("SELECT * FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            user = curs.fetchone()
            if not user:
                curs.execute("INSERT INTO users (telegram_id, name, keywords, send_time) VALUES ('{}', '{}', '', '{}')".format(id, name, datetime.now()))
                send_message('Новий запис в базу даних!', chat)
                conn.commit()
            send_message('Етап реєстрації успішно пройдений. Ваші дані:', chat)
            send_message(text, chat)
        elif text.startswith('/keywords'):
            curs = conn.cursor()
            curs.execute("SELECT keywords FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            present_words = curs.fetchone()[0]
            text = text.split(' ')
            text.pop(0)
            text = ' '.join(text)
            curs.execute("UPDATE users SET keywords ='{}' WHERE telegram_id ='{}' AND name ='{}'".format(str(present_words + ', ' + text), id, name))
            conn.commit()
            send_message('Ключові слова змінено! Ваш список: ' + str(present_words + ', ' + text), chat)
        else:
            send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
