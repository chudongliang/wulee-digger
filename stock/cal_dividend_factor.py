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

client = MongoClient('127.0.0.1', 27017)

stock = client.stock
fundamental = stock.fundamental
corporate_action = stock.corporate_action
corporate_action.create_index( [("id", 1), ("date", 1)], unique=True)
daily_price = stock.daily_price


for v in fundamental.find({'id':'600000'}, no_cursor_timeout=True):
    total_factor = 1
    for v1 in corporate_action.find({'id':v['id']}, no_cursor_timeout=True).sort("date", 1):
        if (('stock_dividend' in v1) and (v1['stock_dividend'] or v1['capital_dividend'] or v1['cash_dividend'])) or v1['allotment_amount']:
            close_price = daily_price.find({'id':v['id'],'date':{'$lte':v1['date']}}, no_cursor_timeout=True).sort("date", -1)

            if 'stock_dividend' in v1:
                factor = float(close_price[0]['close'])* (1 + float(v1['stock_dividend'])/10 + float(v1['capital_dividend'])/10)/(float(close_price[0]['close']) - float(v1['cash_dividend'])/10)
                #factor = round(factor,3)
            if 'allotment_amount' in v1:
                factor = float(close_price[0]['close']) * (1 + float(v1['allotment_amount']) / 10) / (
                         float(close_price[0]['close']) + float(v1['allotment_amount']) / 10 * float(v1['allotment_price']))
                #factor = round(factor, 3)

            total_factor = total_factor * factor
            #total_factor = round(total_factor, 3)
            print(str(v1['date']) + "   "+close_price[0]['close']+"   "+ str(total_factor))

            #print(close_price[0]['close'])

    exit()
                    #post = {'$set': {'id': stock_id, 'date': date,
                    #                 'allotment_amount': row.xpath('td[2]/text()').extract_first(),
                    #                 'allotment_price': row.xpath('td[3]/text()').extract_first(),
                    #                 'allotment_base_share': row.xpath('td[4]/text()').extract_first()}}
                    #query = {'id': stock_id, 'date': date}
                    #post_id = corporate_action.update_one(query, post, True)
