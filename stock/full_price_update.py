# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
from pymongo import MongoClient

from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast
import sys

from news import test

test.c()
import settings

client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

db = client.temporary
collection = db.price_url

stock = client.stock
daily_price = stock.daily_price
daily_price.create_index( [("id", 1), ("date", 1)], unique=True)

class FullPriceSpider(scrapy.Spider):

    name = 'full_price_spider'

    start_urls = []
    for v in collection.find({}, no_cursor_timeout=True):
        start_urls.append('http://' + v['url'])

    def parse(self, response):

        if b'data' in response.body:
            code = response.body.split(b'code\":\"')
            code = code.pop()
            code = code.split(b'\"')
            code = code[0]


            s = response.body.split(b'data\":[\"')
            temp = s.pop()
            temp = temp.strip(b'\"]})')

            items = temp.split(b'\",\"')
            for k in items:

                item = k.split(b',')

                query = {'id': code.decode('utf-8'), 'date': item[0].decode('utf-8')}
                exist = daily_price.find_one(query)
                if not exist:
                    if len(item)>8:
                        post = { '$set': { 'id': code.decode('utf-8') , 'date': item[0].decode('utf-8')
                            , 'open': item[1].decode('utf-8')
                            , 'close': item[2].decode('utf-8')
                            , 'high': item[3].decode('utf-8')
                            , 'low': item[4].decode('utf-8')
                            , 'volume': item[5].decode('utf-8')
                            , 'amount': item[6].decode('utf-8')
                            , 'amplitude': item[7].decode('utf-8')
                            , 'turnover': item[8].decode('utf-8')} }
                    else:
                        post = {'$set': {'id': code.decode('utf-8'), 'date': item[0].decode('utf-8')
                            , 'open': item[1].decode('utf-8')
                            , 'close': item[2].decode('utf-8')
                            , 'high': item[3].decode('utf-8')
                            , 'low': item[4].decode('utf-8')
                            , 'volume': item[5].decode('utf-8')
                            , 'amount': item[6].decode('utf-8')
                            , 'amplitude': item[7].decode('utf-8')
                            , 'turnover': ''}}
                    query = {'id': code.decode('utf-8') , 'date': item[0].decode('utf-8')}
                    post_id = daily_price.update_one(query,post,True)
