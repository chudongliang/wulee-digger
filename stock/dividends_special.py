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

import settings
import datetime
client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

stock = client.stock
fundamental = stock.fundamental
dividend = stock.dividend
dividend.create_index( [("id", 1), ("date", 1)], unique=True)

class FullCorporateSpecialActionSpider(scrapy.Spider):

    name = 'full_corporate_special_action'

    start_urls = []
    for v in fundamental.find({}, no_cursor_timeout=True):
        url = 'http://stock.jrj.com.cn/share,'+v['id']+',fhsp.shtml'
        start_urls.append(url)

    def parse(self, response):

        part1 = response.xpath("/html/body/div/div[2]/div[2]/table/tbody/tr/td[2]/div/table[1]/tbody/tr")
        if len(part1) > 0:
            #print(response.request.url)
            #print(len(part1))
            request_url = response.request.url
            stock_id = request_url.split('share')
            stock_id = stock_id[1][1:7]

            for row in part1:
                #// *[ @ id = "sharebonus_1"] / tbody / tr[1] / td[1]
                if row.xpath('td[6]/text()').extract_first()=='实施':
                    date = row.xpath('td[7]/text()').extract_first()

                    datestring = date.split('-')
                    date = datetime.datetime(int(datestring[0]), int(datestring[1]), int(datestring[2]))

                    query = {'id': stock_id, 'date': date}
                    exist = dividend.find_one(query)
                    if not exist:
                        print(date)
                        print(stock_id)

                        if row.xpath('td[4]/text()').extract_first().strip()=='--':
                            stock_dividend = 0
                        else:
                            stock_dividend = float(row.xpath('td[4]/text()').extract_first())

                        if row.xpath('td[5]/text()').extract_first().strip()=='--':
                            capital_dividend = 0
                        else:
                            capital_dividend = float(row.xpath('td[5]/text()').extract_first())

                        if row.xpath('td[3]/text()').extract_first().strip()=='--':
                            cash_dividend = 0
                        else:
                            cash_dividend = float(row.xpath('td[3]/text()').extract_first())

                        post = {'$set': {'id': stock_id, 'date': date,
                            'stock_dividend': stock_dividend,
                            'capital_dividend': capital_dividend,
                            'cash_dividend': cash_dividend,
                            'allotment_amount':0,
                            'allotment_price':0,
                            'allotment_base_share':0,
                            'source':'jrj'}}
                        query = {'id': stock_id, 'date': date}
                        #print(post)
                        post_id = dividend.update_one(query, post, True)

