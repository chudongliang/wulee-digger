# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
from scrapy.http.request import Request
from pymongo import MongoClient
from scrapy.conf import settings
import json

from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast
import sys

from news import test

test.c()
#import settings
#client = MongoClient(settings.MONGO_HOSTNAME, settings.MONGO_PORT)

client = MongoClient("127.0.0.1",27017)
db = client.temporary
collection = db.price_url


class LakmeSampleItem(scrapy.Item):
    urls = scrapy.Field()

stock = client.stock
ticker_price = stock.ticker_price
ticker_price.create_index( [("id", 1), ("date", 1)], unique=True)








class TickerPriceSpider(scrapy.Spider):

    name = 'ticker_price_spider'


    daily_price = stock.daily_price
    daily_price = daily_price.find({'date': {'$gt': '2018-08-11', '$lt': '2018-09-15'}}, no_cursor_timeout=True).sort('date',1)
    crawl_date = []
    for v in daily_price:
        crawl_date.append([v['date'],v['id']])

    loop = True
    while loop:
        stock_detail = crawl_date.pop()
        check_exist = ticker_price.find_one({'id': stock_detail[1], 'date': stock_detail[0]}, no_cursor_timeout=True)
        if not check_exist or check_exist['data'] == '[]':
            loop = False

    stock_id = stock_detail[1]
    stock_date = stock_detail[0]
    i = 1
    page = str(i)

    m = ""
    if stock_id[0:1]=='6':
        m = 'sh'
    else:
        m = 'sz'

    start_urls = ['http://market.finance.sina.com.cn/transHis.php?symbol='+m+stock_id+'&date='+stock_detail[0]+'&page='+page]

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
            post = {'$set': {'id': self.stock_id, 'date': self.stock_date, 'data': json_string}}
            query = {'id': self.stock_id, 'date': self.stock_date}
            post_id = ticker_price.update_one(query, post, True)

            self.val = []
            self.i = 1

            loop = True
            while loop:
                stock_detail = self.crawl_date.pop()
                check_exist = ticker_price.find_one({'id': stock_detail[1], 'date': stock_detail[0]},no_cursor_timeout=True)
                if not check_exist or check_exist['data'] == '[]':
                    loop = False

            self.stock_id = stock_detail[1]
            self.stock_date = stock_detail[0]


            if stock_detail[1][0:1] == '6':
                self.m = 'sh'
            else:
                self.m = 'sz'

            url = 'http://market.finance.sina.com.cn/transHis.php?symbol='+self.m+stock_detail[1]+'&date=' + stock_detail[0] + '&page=1'
            request = Request(str(url), callback=self.parse)
            yield request
            #print(json_string)
            print('end')


class TickerTodayPriceSpider(scrapy.Spider):


    name = 'ticker_today_price_spider'

    fundamental = stock.fundamental
    result = fundamental.find({}, no_cursor_timeout=True)

    stock_list = []
    for stock_detail in result:
        stock_list.append([stock_detail['id'],stock_detail['market']])

    start_urls = ['http://gu.qq.com/sh000001/zs']
    date = ""
    page = 0
    market_name = ""
    stock_id = ""
    val = []


    def parse(self, response):
        stats = response.xpath('//*[@id="tagStat"]/a/text()').extract_first()
        if stats == '已休市' or stats == '已收盘' or stats == '未开盘':
            date_string = response.body.split(b'\"hq\":[\"')
            self.date = date_string[1][0:4].decode('utf-8')+'-'+date_string[1][4:6].decode('utf-8')+'-'+date_string[1][6:8].decode('utf-8')

            loop = True
            while loop:
                stock_detail = self.stock_list.pop()
                check_exist = ticker_price.find_one({'id': stock_detail[0], 'date': self.date}, no_cursor_timeout=True)
                if not check_exist or check_exist['data'] == '[]':
                    loop = False

            if stock_detail[1] == '2':
                self.market_name = 'sz';
            if stock_detail[1] == '1':
                self.market_name = 'sh';


            url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c='+self.market_name+stock_detail[0]+'&p='+str(self.page)

            self.stock_id = stock_detail[0]
            self.page += 1
            request = Request(str(url), callback=self.parse)
            yield request

        if b'v_detail_data' in response.body:

            date_string = response.body.split(b'\"')
            date_string = date_string[1].split(b'|')
            for string in date_string:
                string = string.split(b'/')

                if string[3].decode('utf-8') == '0.00':
                    change = '0'
                else:
                    change = string[3].decode('utf-8')

                if string[6].decode('utf-8') == 'B':
                    type = '1'
                elif string[6].decode('utf-8') == 'S':
                    type = '2'
                elif string[6].decode('utf-8') == 'M':
                    type = '3'

                item = [string[1].decode('utf-8'),
                        string[2].decode('utf-8'),
                        change,
                        string[4].decode('utf-8'),
                        string[5].decode('utf-8'),
                        type]

                self.val.append(item)

            url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=' + self.market_name + self.stock_id + '&p=' + str(self.page)
            self.page += 1
            request = Request(str(url), callback=self.parse)
            yield request

        if not response.body:

            json_string = json.dumps(self.val)
            post = {'$set': {'id': self.stock_id, 'date': self.date, 'data': json_string}}
            query = {'id': self.stock_id, 'date': self.date}

            #print(post)
            post_id = ticker_price.update_one(query, post, True)

            self.val = []

            self.page = 0

            loop = True
            while loop:
                stock_detail = self.stock_list.pop()
                check_exist = ticker_price.find_one({'id': stock_detail[0], 'date': self.date}, no_cursor_timeout=True)
                if not check_exist or check_exist['data'] == '[]':
                    loop = False

            if stock_detail[1] == '2':
                self.market_name = 'sz';
            if stock_detail[1] == '1':
                self.market_name = 'sh';
            self.stock_id = stock_detail[0]

            url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=' + self.market_name + self.stock_id + '&p=' + str(self.page)

            self.page += 1
            request = Request(str(url), callback=self.parse)
            yield request
            print("end")
