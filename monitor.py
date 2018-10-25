import json
import re
import sys
from pymongo import MongoClient
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
import scrapy
from scrapy.crawler import CrawlerProcess



client = MongoClient('127.0.0.1', 27017)

stock = client.stock
daily_price = stock.daily_price
#daily_price.

# check trade date : http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18306405097731678042_1539809188322&id=0000011&type=k&authorityType=ba&_=1539809191695

# check market is closed
# http://gu.qq.com/sh000001/zs

class MonitorSpider(scrapy.Spider):

    name = 'monitor_spider'

    custom_settings = {
        'SPIDER_MIDDLEWARES' : {
            'monitor.SaveErrorsMiddleware': 1000,
        }
    }

    start_urls = ['http://gu.qq.com/sh000001/zs','http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18306405097731678042_1539809188322&id=0000011&type=k&authorityType=ba&_=1539809191695']

    def parse(self, response):

        print(response.status)

        if b'data' in response.body:
            code = response.body.split(b'code\":\"')
            code = code.pop()
            code = code.split(b'\"')
            code = code[0]


            s = response.body.split(b'data\":[\"')
            temp = s.pop()
            temp = temp.strip(b'\"]})')

            items = temp.split(b'\",\"')

from scrapy import signals

class SaveErrorsMiddleware(object):
    def __init__(self, crawler):
        crawler.signals.connect(self.close_spider, signals.spider_closed)
        crawler.signals.connect(self.open_spider, signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        print(11)
        #self.output_file = open('./somefile.txt', 'w')

    def close_spider(self, spider):
        print(11)
        #self.output_file.close()

    def process_spider_exception(self, response, exception, spider):
        print('444')
        #sys.exit(-1)
        #if (response.status != 200):
        #    print('444')
        #    sys.exit(-1)
        #self.output_file.write(response.url + '\n')

process = CrawlerProcess()

process.crawl(MonitorSpider())

process.start()