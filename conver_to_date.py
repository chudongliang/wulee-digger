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
import datetime


client = MongoClient("127.0.0.1",27017)
db = client.stock
corporate_action = db.corporate_action
dividend = db.dividend
dividend.create_index( [("id", 1), ("date", 1)], unique=True)


for v in corporate_action.find({},no_cursor_timeout=True):
    print(v['date'])
    datestring = v['date'].split('-')
    date = datetime.datetime(int(datestring[0]), int(datestring[1]), int(datestring[2]))

    print(v['date'])
    if 'allotment_amount' in v:
        allotment_amount = float(v['allotment_amount'])
    else:
        allotment_amount = 0

    if 'stock_dividend' in v:
        stock_dividend = float(v['stock_dividend'])
    else:
        stock_dividend = 0

    if 'capital_dividend' in v:
        capital_dividend = float(v['capital_dividend'])
    else:
        capital_dividend = 0

    if 'cash_dividend' in v:
        cash_dividend = float(v['cash_dividend'])
    else:
        cash_dividend = 0

    if 'allotment_price' in v:
        allotment_price = float(v['allotment_price'])
    else:
        allotment_price = 0

    if 'allotment_base_share' in v:
        allotment_base_share = float(v['allotment_base_share'])
    else:
        allotment_base_share = 0

    post = {'$set': {'id': v['id'], 'date': date
        , 'stock_dividend': stock_dividend
        , 'capital_dividend': capital_dividend
        , 'cash_dividend': cash_dividend
        , 'allotment_amount': allotment_amount
        , 'allotment_price': allotment_price
        , 'allotment_base_share': allotment_base_share}}
    query = {'id': v['id'], 'date': date}
    post_id = dividend.update_one(query, post, True)




