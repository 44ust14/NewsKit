# -*-coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import os
from bs4 import BeautifulSoup
import requests
import lxml
import scrapy
#from wylsacom_scrapy import wylsacom
#from wylsacom import parse_wylsacom
import psycopg2
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from two_four_tvua import parse_24tvua


os.environ['DATABASE_URL'] = 'postgres://aszcitgpnlvywd:724a92d4dd1cdb044882cb6f579060b8482e7da45191194cf9b5c7677bc9f210@ec2-54-247-81-88.eu-west-1.compute.amazonaws.com:5432/dfq1utl6uns158'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

curs = conn.cursor()
# def func():
#     wylsacom = parse_wylsacom()
#     print(wylsacom)
#
#     links = []
#     for item in wylsacom:
#         link = item['link']
#         links.append(link)
#
#     curs.execute("SELECT * FROM articles WHERE website_id ='{}' ORDER BY ID DESC LIMIT 1".format(1))
#     last_article = curs.fetchone()
#
#     print(links)
#     print(last_article)
#
#     if last_article[2] in links:
#         index = links.index(last_article[2])
#         for new_article_number in range(0, index):
#             print(new_article_number)
#             new_article = wylsacom[new_article_number]
#
#             curs.execute("INSERT INTO articles (website_id, url, article_date, keywords, parse_time)  VALUES ('{}','{}', '{}','{}', '{}')".format('1', new_article['link'], new_article['date'], '', datetime.now()))
#             conn.commit()
#
#             requests.get('https://api.telegram.org/bot582815834:AAFkPhSrT-yfSq0Vi6dI8bMTFXovoVWT0Ok/sendMessage?chat_id=138918380&text={}'.format(new_article['link']))
#
#
# func()








# curs = conn.cursor()
# curs.execute("INSERT INTO websites (url, names)  VALUES ('{}','{}')".format('https://wylsa.com/', 'wylsa, wylsacom, вилса, вилсаком, вілса, вілсаком'))
#
# conn.commit()



def two_four_tvua():
    two_four_tvua = parse_24tvua()
    print(two_four_tvua)

    links = []
    for item in two_four_tvua:
        link = item['link']
        links.append(link)

    curs.execute("SELECT * FROM articles WHERE website_id ='{}' ORDER BY ID DESC LIMIT 1".format(2))
    last_article = curs.fetchone()

    print(links)
    print(last_article)

    if last_article[2] in links:
        index = links.index(last_article[2])
        print('index', index)

        for new_article_number in range(index-1, -1, -1):
            print(new_article_number)
            new_article = two_four_tvua[new_article_number]

            #defining article keywords by its header
            title = remove_bad_characters(new_article['title'].split(' '))

            curs.execute("SELECT keywords FROM users")
            keywords_all = list(curs.fetchall())
            keywords_all_new = []
            for words in keywords_all:
                el_list = words[0].split(', ')
                keywords_all_new = keywords_all_new  + el_list

            keywords_all = []
            for i in keywords_all_new:
                if i not in keywords_all and i != '':
                    keywords_all.append(i)

            print('all keywords:', keywords_all)
            #endof getting all keywords list, we get keywords_all variable with all of them

            #comparing title words with already existing keywords
            article_keywords = []
            for word in title:
                if word in keywords_all:
                    article_keywords.append(word)

            print('title', title)
            print('keywords in article: ', article_keywords)

            article_keywords = ', '.join(article_keywords)

            curs.execute("INSERT INTO articles (website_id, url, article_date, keywords, parse_time)  VALUES ('{}','{}', '{}','{}', '{}')".format('2', new_article['link'], new_article['date'], article_keywords, datetime.now()))
            conn.commit()

            curs.execute("SELECT telegram_id, status, keywords FROM users")

            users = list(curs.fetchall())

            for user in users:
                chat_id = user[0]
                status = user[1]
                user_keywords = user[2].split(', ')
                print(chat_id, status, user_keywords)
                passed_keywords = []
                for word in user_keywords:
                    if word in article_keywords:
                        passed_keywords.append(word)

                passed_keywords = ', '.join(passed_keywords)
                print('passed_keywords: ', passed_keywords)
                if int(status) == 0 and passed_keywords != '':
                    print(True)
                    requests.get('https://api.telegram.org/bot577877864:AAEh1MKE62KPntQjSuEtH53sDYJDes3oYyM/sendMessage?chat_id={}&text={}'.format(chat_id, '(хероку) Знайдено такі ключові слова у наступній статті: ' + passed_keywords + '\n' + new_article['link']))
    else:
        for new_article_number in range(len(links)-1, -1, -1):
            print(new_article_number)
            new_article = two_four_tvua[new_article_number]

            #defining article keywords by its header
            title = remove_bad_characters(new_article['title'].split(' '))

            curs.execute("SELECT keywords FROM users")
            keywords_all = list(curs.fetchall())
            keywords_all_new = []
            for words in keywords_all:
                el_list = words[0].split(', ')
                keywords_all_new = keywords_all_new  + el_list

            keywords_all = []
            for i in keywords_all_new:
                if i not in keywords_all and i != '':
                    keywords_all.append(i)

            print('all keywords:', keywords_all)
            #endof getting all keywords list, we get keywords_all variable with all of them

            #comparing title words with already existing keywords
            article_keywords = []
            for word in title:
                if word in keywords_all:
                    article_keywords.append(word)

            print('title', title)
            print('keywords in article: ', article_keywords)

            article_keywords = ', '.join(article_keywords)

            curs.execute("INSERT INTO articles (website_id, url, article_date, keywords, parse_time)  VALUES ('{}','{}', '{}','{}', '{}')".format('2', new_article['link'], new_article['date'], article_keywords, datetime.now()))
            conn.commit()

            curs.execute("SELECT telegram_id, status, keywords FROM users")

            users = list(curs.fetchall())

            for user in users:
                chat_id = user[0]
                status = user[1]
                user_keywords = user[2].split(', ')
                print(chat_id, status, user_keywords)
                passed_keywords = []
                for word in user_keywords:
                    if word in article_keywords:
                        passed_keywords.append(word)

                passed_keywords = ', '.join(passed_keywords)
                print('passed_keywords: ', passed_keywords)
                if int(status) == 0 and passed_keywords != '':
                    print(True)
                    requests.get('https://api.telegram.org/bot577877864:AAEh1MKE62KPntQjSuEtH53sDYJDes3oYyM/sendMessage?chat_id={}&text={}'.format(chat_id, '(хероку) Знайдено такі ключові слова у наступній статті: ' + passed_keywords + '\n' + new_article['link']))



def remove_bad_characters(list):
    # for ch in [',',' ', ':', '-', '"', '!']:
    #     for string in list:
    #         if ch in string:
    #             list = [string.replace(ch,"\\"+ch)]
    list = [s.replace(',', '') for s in list]
    list = [s.replace(' ', '') for s in list]
    list = [s.replace(':', '') for s in list]
    list = [s.replace('–', '') for s in list]
    list = [s.replace('!', '') for s in list]
    list = [s.replace('"', '') for s in list]
    list = [s.lower() for s in list]
    return list

two_four_tvua()



sched = BlockingScheduler()

cur_website = 1

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')
    two_four_tvua()

    # parse cur_website
    #if cur_website == 1:
        #print(wylsacom())
        #parsing




# @sched.scheduled_job('cron', hour=13)
# def scheduled_job():
#     print('This job is run every weekday at 1pm.')

sched.start()







app = Flask(__name__)
app.secret_key = 'super secret key'









if __name__ =='__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(port=5003)
