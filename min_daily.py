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
from stock import min_price_update

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(min_price_update.MinPriceDailySpider())
    #yield runner.crawl(ticker.TickerTodayPriceSpider())
    reactor.stop()

crawl()
reactor.run()
