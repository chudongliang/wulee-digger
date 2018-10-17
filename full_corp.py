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
from stock import dividends_special

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    #dividends.FullCorporateActionSpider.download_delay = 1.2
    #yield runner.crawl(dividends.FullCorporateActionSpider())

    dividends_special.FullCorporateSpecialActionSpider.download_delay = 1.2
    yield runner.crawl(dividends_special.FullCorporateSpecialActionSpider())
    reactor.stop()

crawl()
reactor.run()
