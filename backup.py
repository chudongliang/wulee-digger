from __future__ import division
import scrapy
from scrapy.crawler import CrawlerProcess
import base64
from pymongo import MongoClient


import re
import math
import json
import gzip
import ast

import sys
from hamcrest.core.core.isnone import none
sys.path.insert(0, '/stock/')
sys.path.insert(0, '/news/')

#from data.stock.min_price import MinPrice

#a = MinPrice(2,'2',4)

#print(type(a.id))
#exit()

#process = CrawlerProcess({
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
#    #'DOWNLOAD_DELAY': 1,
#    #'RETRY_HTTP_CODES': {500, 502, 503, 504, 522, 524, 408, 456},
#    'COOKIES_ENABLED': False
#})

#from stock import fun
#process.crawl(fun.FunSpider())
#process.start(stop_after_crawl=False)


process1 = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    #'DOWNLOAD_DELAY': 1,
    #'RETRY_HTTP_CODES': {500, 502, 503, 504, 522, 524, 408, 456},
    #'CONCURRENT_REQUESTS_PER_IP': 32,
    #'CONCURRENT_REQUESTS_PER_DOMAIN':32,
    #'COOKIES_ENABLED': False
    #'COOKIES_ENABLED': False
})
from stock import ticker
ticker.TickerTodayPriceSpider.CONCURRENT_REQUESTS_PER_IP = 4
process1.crawl(ticker.TickerTodayPriceSpider())

process1.crawl(ticker.TickerTodayPriceSpider1())

process1.crawl(ticker.TickerTodayPriceSpider2())

process1.crawl(ticker.TickerTodayPriceSpider3())

from stock import full_price_update
process1.crawl(full_price_update.FullPriceSpider())

from stock import min_price_update
process1.crawl(min_price_update.MinPriceDailySpider())

process1.start()