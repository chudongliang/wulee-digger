# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
from pymongo import MongoClient
import datetime
from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast
import sys

import settings

client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

stock = client.stock
fundamental = stock.fundamental
dividend = stock.dividend
dividend.create_index( [("id", 1), ("date", 1)], unique=True)

class FullCorporateActionSpider(scrapy.Spider):

    name = 'full_corporate_action'

    start_urls = []
    for v in fundamental.find({}, no_cursor_timeout=True):
        url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/'+v['id']+'.phtml'
        start_urls.append(url)

    def parse(self, response):
        print(response.request.url)
        part1 = response.xpath('// *[ @ id = "sharebonus_1"] / tbody / tr')
        if len(part1) > 0:

            request_url = response.request.url
            stock_id = request_url.split('stockid')
            stock_id = stock_id[1][1:7]

            for row in part1:
                #// *[ @ id = "sharebonus_1"] / tbody / tr[1] / td[1]
                if row.xpath('td[5]/text()').extract_first()=='实施':
                    date = row.xpath('td[7]/text()').extract_first()

                    datestring = date.split('-')
                    if int(datestring[0])>0:
                        date = datetime.datetime(int(datestring[0]), int(datestring[1]), int(datestring[2]))

                        post = {'$set': {'id': stock_id, 'date': date,
                                         'stock_dividend': float(row.xpath('td[2]/text()').extract_first()),
                                         'capital_dividend': float(row.xpath('td[3]/text()').extract_first()),
                                         'cash_dividend': float(row.xpath('td[4]/text()').extract_first()),
                                         'allotment_amount':0,
                                         'allotment_price':0,
                                         'allotment_base_share':0}}
                        query = {'id': stock_id, 'date': date}
                        post_id = dividend.update_one(query, post, True)

        part2 = response.xpath('// *[ @ id = "sharebonus_2"] / tbody / tr')
        if len(part2) > 0:

            request_url = response.request.url
            stock_id = request_url.split('stockid')
            stock_id = stock_id[1][1:7]

            for row in part2:
                # // *[ @ id = "sharebonus_1"] / tbody / tr[1] / td[1]
                if row.xpath('td[6]/text()').extract_first():
                    date = row.xpath('td[6]/text()').extract_first()

                    datestring = date.split('-')
                    date = datetime.datetime(int(datestring[0]), int(datestring[1]), int(datestring[2]))

                    post = {'$set': {'id': stock_id, 'date': date,
                                     'stock_dividend':0,
                                     'capital_dividend':0,
                                     'cash_dividend':0,
                                     'allotment_amount': float(row.xpath('td[2]/text()').extract_first()),
                                     'allotment_price': float(row.xpath('td[3]/text()').extract_first()),
                                     'allotment_base_share': float(row.xpath('td[4]/text()').extract_first())}}
                    query = {'id': stock_id, 'date': date}
                    post_id = dividend.update_one(query, post, True)
