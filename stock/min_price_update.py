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
import datetime
client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

db = client.temporary
collection = db.price_url

db1 = client.stock
min_price = db1.min_price
min_price.create_index( [("id", 1), ("date", 1)], unique=True)

#from data.stock.min_price import MinPrice

class MinPriceDailySpider(scrapy.Spider):

    name = 'min_price_daily_spider'

    start_urls = []
    for v in collection.find({}, no_cursor_timeout=True):
        start_urls.append('http://' + v['url'].replace("type=k","type=m1"))

    def parse(self, response):

        if not b'stats:false' in response.body:

            request_url = response.request.url
            stock_id = request_url.split('id=')
            stock_id = stock_id[1][0:6]




            code = response.body.split(b'\r\n')

            for row in code:

                row = row.split(b',')

                date_time = row[0].split(b' ')
                date_time = date_time[1].split(b':')
                date_time = datetime.datetime.combine(datetime.date.today(), datetime.time(int(date_time[0].decode('utf-8')), int(date_time[1].decode('utf-8'))))

                start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(9, 30))
                end_time = datetime.datetime.combine(datetime.date.today(), datetime.time(15,0))

                if date_time>start_time and date_time<=end_time:



                    post = {'$set': {'id': stock_id, 'date': date_time
                        , 'open': float(row[1].decode('utf-8'))
                        , 'close': float(row[4].decode('utf-8'))
                        , 'high': float(row[2].decode('utf-8'))
                        , 'low': float(row[3].decode('utf-8'))
                        , 'volume': float(row[6].decode('utf-8'))
                        , 'amount': float(row[7].decode('utf-8'))}}
                    query = {'id': stock_id, 'date': date_time}
                    post_id = min_price.update_one(query, post, True)

                    #print(row[0])






                #post_id = daily_price.update_one(query,post,True)
