# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
from scrapy.http.request import Request
from pymongo import MongoClient
#from scrapy.conf import settings
import json

from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast
import sys
import psycopg2
#import settings
#client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

import datetime

from common.db import Postgres

db = Postgres()

class TickerPriceSpider(scrapy.Spider):

    name = 'ticker_price_spider'

    #start_date = datetime.datetime(2019, 1, 20)
    #end_date = datetime.datetime(2019, 2, 2)

    #print(start_date)
    #exit
    #daily_price = stock.daily_price
    #daily_price = daily_price.find({'date': {'$gt': start_date, '$lt': end_date}}, no_cursor_timeout=True).sort('date',1)
    
    daily_price = db.fetchall("SELECT * from source.daily_price where date>'2019-01-01' AND date<'2019-03-02' order by date DESC")
        

    crawl_date = []
    for v in daily_price:
        crawl_date.append([v[0],v[8]])

    loop = True
    while loop:
        stock_detail = crawl_date.pop()
        date_string = str(stock_detail[0]).split(" ")

        #check_exist = ticker_price.find_one({'id': stock_detail[1], 'date': date_string[0]}, no_cursor_timeout=True)
        check_exist = db.fetchone("SELECT * from source.ticker_price where id=%s AND date=%s", (stock_detail[1],stock_detail[0],))
        
        if check_exist is None or check_exist[2] == '[]':
        #if not check_exist or check_exist['data'] == '[]':
            loop = False

    stock_id = stock_detail[1]
    stock_date = date_string[0]
    
    i = 1
    page = str(i)

    m = ""
    if stock_id[0:1]=='6':
        m = 'sh'
    else:
        m = 'sz'

    start_urls = ['http://market.finance.sina.com.cn/transHis.php?symbol='+m+stock_id+'&date='+date_string[0]+'&page='+page]

    val = []

    def parse(self, response):

        #print(response.body)
        if (b'<h5>' in response.body) or (b'<h6>' in response.body) or (b'<h1>' in response.body):
            self.i += 1
            page = str(self.i)

            products = response.xpath('//*[@id="datatbl"]/tbody/tr')
            for row in products:
                if row.xpath('th[2]/h6/text()').extract_first() == '卖盘':
                    type = '1'
                elif row.xpath('th[2]/h5/text()').extract_first() == '买盘':
                    type = '2'
                elif row.xpath('th[2]/h1/text()').extract_first() == '中性盘':
                    type = '3'


                if row.xpath('td[2]/text()').extract_first() == '--':
                    change = '0'
                else:
                    change = row.xpath('td[2]/text()').extract_first()

                item = [row.xpath('th[1]/text()').extract_first(),
                        row.xpath('td[1]/text()').extract_first(),
                        change,
                        row.xpath('td[3]/text()').extract_first(),
                        row.xpath('td[4]/text()').extract_first().replace(",", ""),
                        type]

                self.val.insert(0, item)

            url = 'http://market.finance.sina.com.cn/transHis.php?symbol='+self.m+self.stock_id+'&date='+self.stock_date+'&page='+page
            request = Request(str(url), callback=self.parse)
            yield request
        else:

            json_string = json.dumps(self.val)
            #post = {'$set': {'id': self.stock_id, 'date': self.stock_date, 'data': json_string}}
            #query = {'id': self.stock_id, 'date': self.stock_date}
            
            postgres_insert_query = "INSERT INTO source.ticker_price (id,date,data) VALUES (%s,%s,%s)"
            record_to_insert = (self.stock_id, self.stock_date, json_string,)
            db.insert(postgres_insert_query, record_to_insert)
            db.commit()
            
            #print(json_string)
            #exit()
            #post_id = ticker_price.update_one(query, post, True)

            self.val = []
            self.i = 1

            loop = True
            while loop:
                stock_detail = self.crawl_date.pop()
                date_string = str(stock_detail[0]).split(" ")
                #check_exist = ticker_price.find_one({'id': stock_detail[1], 'date': date_string[0]},no_cursor_timeout=True)
                
                check_exist = db.fetchone("SELECT * from source.ticker_price where id=%s AND date=%s", (stock_detail[1],stock_detail[0],))
                if check_exist is None or check_exist[2] == '[]':
                    loop = False

            self.stock_id = stock_detail[1]
            self.stock_date = date_string[0]


            if stock_detail[1][0:1] == '6':
                self.m = 'sh'
            else:
                self.m = 'sz'

            url = 'http://market.finance.sina.com.cn/transHis.php?symbol='+self.m+stock_detail[1]+'&date=' + date_string[0] + '&page=1'
            request = Request(str(url), callback=self.parse)
            yield request
            print('end')
