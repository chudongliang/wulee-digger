from __future__ import division
import scrapy
from scrapy.crawler import CrawlerProcess
import base64
from pymongo import MongoClient
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import re
import math
import json
import gzip
import ast

import sys
sys.path.insert(0, '/stock/')
sys.path.insert(0, '/news/')
from stock import fun

configure_logging()
runner = CrawlerRunner()

from stock import ticker
#ticker.TickerPriceSpider.download_delay = 1.2
#process1.crawl(ticker.TickerPriceSpider())
#ticker.TickerTodayPriceSpider.CONCURRENT_REQUESTS_PER_IP = 2
#process1.crawl(ticker.TickerTodayPriceSpider())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ticker.TickerTodayPriceSpider())
    reactor.stop()

crawl()
reactor.run()
