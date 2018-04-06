#encoding: UTF-8
import json
import requests
import time
from datetime import datetime
import urllib
import psycopg2
import os
import telepot



os.environ['DATABASE_URL'] = 'postgres://aszcitgpnlvywd:724a92d4dd1cdb044882cb6f579060b8482e7da45191194cf9b5c7677bc9f210@ec2-54-247-81-88.eu-west-1.compute.amazonaws.com:5432/dfq1utl6uns158'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


TOKEN = '577877864:AAEh1MKE62KPntQjSuEtH53sDYJDes3oYyM'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

PORT = int(os.environ.get('PORT', '8443'))

TelegramBot = telepot.Bot(TOKEN)


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
        text = text.lower()

        chat = update["message"]["chat"]["id"]

        id = update['message']['chat']['id']
        name =  update['message']['chat']['first_name']

        if text == '/start':
            text = 'Тебе вітає NewsKit!'
            send_message(text, chat)

            #text = str([update['message']['chat']['id'], update['message']['chat']['first_name']])
            curs = conn.cursor()
            curs.execute("SELECT * FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            user = curs.fetchone()
            if not user:
                curs.execute("INSERT INTO users (telegram_id, name, keywords, send_time, status) VALUES ('{}', '{}', '', '{}', 0)".format(id, name, datetime.now()))
                send_message('Ти успішно записаний в базу даних!', chat)
                conn.commit()
            send_message('Етап реєстрації пройдений! Ура!', chat)
            #send_message(text, chat)
            send_help(text, chat)
        elif text.startswith('/keywords') or text.startswith('/add') or text.startswith('/додай') or text.startswith('ключові слова:'):
            if text.startswith('ключові слова:'):
                text = text.split(' ')
                text.pop(0)
                text.pop(0)
            else:
                text = text.split(' ')
                text.pop(0)
            curs = conn.cursor()
            curs.execute("SELECT keywords FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            present_words = curs.fetchone()[0]
            present_words_list = present_words.split(', ')
            present_words_list = remove_bad_characters(present_words_list)

            text = remove_bad_characters(text)
            print(text)
            #text consists of received list of new keywords

            # loop for detecting repeating keywords
            isgoingtoberemoved = []
            for word in text:
                if word in present_words_list:
                    send_message(str(word + ' не додано через повтор'), chat)
                    isgoingtoberemoved.append(word)
                else:
                    send_message(str(word + ' додано'), chat)

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
            curs.execute("UPDATE users SET keywords ='{}' WHERE telegram_id ='{}' AND name ='{}'".format(str(present_words_list + text), id, name))
            conn.commit()
            send_message('Ваш список ключових слів: ' + str(present_words_list + text), chat)
        elif text.startswith('/deletekeywords') or text.startswith('/remove') or text.startswith('/вилучи') or text.startswith('видали ключові слова:') or text.startswith('видалити ключові слова:'):
            if text.startswith('видали ключові слова:') or text.startswith('видалити ключові слова:'):
                text = text.split(' ')
                text.pop(0)
                text.pop(0)
                text.pop(0)
            else:
                text = text.split(' ')
                text.pop(0)
            text = remove_bad_characters(text)
            curs = conn.cursor()
            curs.execute("SELECT keywords FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            present_words = curs.fetchone()[0]
            present_words_list = present_words.split(', ')
            present_words_list = remove_bad_characters(present_words_list)

            #loop for removing chosen elements
            for should_remove in text:
                if should_remove in present_words_list:
                    present_words_list.remove(should_remove)
                    send_message(str(should_remove + ' вилучено'), chat)
                else:
                    send_message(str(should_remove + ' не є твоїм ключовим словом'), chat)

            if len(present_words_list) == 1 and present_words_list[0] == '':
                present_words_list = ''.join(present_words_list)
            else:
                present_words_list = ', '.join(present_words_list)

            curs.execute("UPDATE users SET keywords ='{}' WHERE telegram_id ='{}' AND name ='{}'".format(str(present_words_list), id, name))
            conn.commit()
            send_message('Ваш список ключових слів: ' + str(present_words_list), chat)

        elif text == '/deleteaccount' or text.startswith('/deleteacc') or text.startswith('видалити аккаунт'):
            curs = conn.cursor()
            curs.execute("DELETE FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            conn.commit()

            text = 'Ти більше не отримуватимеш щоденних розсилок(( Щоб відновити цю можливість напиши мені /start'
            send_message(text, chat)
        elif text == '/stop' or text.startswith('stop') or text.startswith('стоп') or text.startswith('стій'):
            curs = conn.cursor()
            curs.execute("SELECT status FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            status = int(curs.fetchone()[0])
            if status != 1:
                curs.execute("UPDATE users SET status = 1 WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
                conn.commit()
                text = 'Ти більше не отримуватимеш щоденних розсилок(( Щоб відновити цю можливість напиши мені /renew'
            else:
                text = 'Ти вже відмовився від отримання новин раніше(( Щоб відновити цю можливість напиши мені /renew'

            send_message(text, chat)

        elif text == '/renew' or text == 'renew' or text.startswith('відновити'):
            curs = conn.cursor()
            curs.execute("SELECT status FROM users WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
            status = int(curs.fetchone()[0])
            if status != 0:
                curs.execute("UPDATE users SET status = 0 WHERE telegram_id ='{}' AND name ='{}'".format(id, name))
                conn.commit()
                text = 'Ти знову зі мною! Тепер ти отримуватимеш щоденну підбірку персоналізованих новин! Гіп-гіп УРА!😍))'
            else:
                text = 'Ти вже погодився на отримання новин раніше! Дякую за довіру!'

            send_message(text, chat)
        elif text == '/help' or text.startswith('help') or text.startswith('допомога'):
             send_help(text, chat)
        else:
            send_message(text, chat)

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

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format('(хероку) ' + text, chat_id)
    get_url(url)

def send_help(text, chat_id):
    text = ' Я є чат-ботом, який надсилатиме тобі підбірку свіжих фільтрованих новин у зручний час з обраних новинних веб-сайтів.\n \n <code>Увага! Я поки знаходжусь в розробці і ти користуєшся MVP (найменшою робочою версією), тому поки я підтримую лише 1 новинний сайт. Чекай оновлення зовсім скоро! </code> \n \n Виявлені баги надсилай до <a href="https://www.facebook.com/dmytro.lopushanskyy">Дмитра Лопушанського</a> або <a href="https://www.facebook.com/mlastovski">Марка Ластовського</a> \n \n <b>Алгоритм:</b> 1) Ти пишеш мені свої ключові слова 2) Як тільки з\'являється нова стаття на сайті <a href="http://24tvua.com/">24 Каналу</a>, яка підійде тобі за ключовими словами, то я одразу надішлю в цей чат посилання на неї!  \n \n <i>Список команд боту:</i> \n \n<b>Початок</b> \n  /start - початок переписки \n \n <b>Додавання ключових слів</b> \n /keywords слово1, слово2, слово3 \n /add слово1, слово2, слово3 \n Додай: слово1, слово2, слово3 \n Клочові слова: слово1, слово2, слово3 \n \n <b>Видалення ключових слів</b> \n /deletekeywords слово1, слово2, слово3 \n /remove слово1, слово2, слово3 \n Вилучи: слово1, слово2, слово3 \n Видали клочові слова: слово1, слово2, слово3 \n \n <b>Припинити надсилання новин</b> \n /stop \n стоп \n stop \n \n <b>Відновити надсилання новин</b> \n /renew \n renew \n відновити \n \n  <b>Видалити свій аккаунт в бота</b> \n /deleteacc \n видалити аккаунт' + \
             '\n \n <b>Допомога</b> \n /help \n help \n допомога '

    send_message_html(text, chat_id)

def send_message_html(text, chat_id):
    TelegramBot.sendMessage(chat_id, text, parse_mode = 'HTML')



def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ =='__main__':
    main()
