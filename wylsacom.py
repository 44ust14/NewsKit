from bs4 import BeautifulSoup
import requests
import lxml
import scrapy


data = requests.get("http://www.wylsa.com").text

soup = BeautifulSoup(data, "lxml")



def parse_wylsacom():
    articles = []

    for title in soup.find_all(itemprop='headline'):
        title_text = title.get_text()
        link = title.parent.get('href')

        author = title.parent.parent.parent.parent.find(itemprop='name').get('content')
        date = title.parent.parent.parent.parent.find(itemprop='datePublished').get('datetime')
        if title and link and author and date:
            article = {
                'title': title_text,
                'link': link,
                'author': author,
                'date': date
            }
        #print(article)
        articles.append(article)

    articles = [i for n, i in enumerate(articles) if i not in articles[n + 1:]]

    return articles
