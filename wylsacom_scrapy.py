import scrapy

class wylsacom(scrapy.Spider):
    name = 'wylsacom'
    start_urls = ['https://wylsa.com/']

    def parse(self, response):
        articles = []
        for title in response.xpath('//span[@itemprop="headline"]'):
            author = title.xpath('../../../../div[@class="mp-article-meta mp-element"]/span[@class="mp-author"]/a/span/span[@itemprop="name"]/text()').extract()
            if author:
                article = {
                    'title': title.xpath('text()').extract()[0],
                    'link': title.xpath('../@href').extract()[0],
                    'author': title.xpath('../../../../div[@class="mp-article-meta mp-element"]/span[@class="mp-author"]/a/span/span[@itemprop="name"]/text()').extract()[0],
                    'date': title.xpath('../../../../div[@class="mp-article-meta mp-element"]/span[@class="mp-date"]/time[@itemprop="datePublished"]/text()').extract()[0]
                }
                print(article)
                articles.append(article)

            #yield response.follow(article['link'], self.parse)

        return articles

    #def get_additional_info(self, article):


