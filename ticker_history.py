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

from stock import ticker_history
ticker_history.TickerPriceSpider.download_delay = 1.2

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ticker_history.TickerPriceSpider())
    reactor.stop()

crawl()
reactor.run()
