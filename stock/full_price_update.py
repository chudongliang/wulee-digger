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
import psycopg2

import settings
import datetime


from data.stock.daily_price import DailyPrice


connection = psycopg2.connect(user="postgres",
                                  password="cmhorse888",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wulee")
cursor = connection.cursor()


class FullPriceSpider(scrapy.Spider):

    name = 'full_price_spider'

    start_urls = []
    
    
    cursor.execute("SELECT * from source.price_url")
    rows = cursor.fetchall()
    
    
    for v in rows:
        start_urls.append('http://' + v[1])

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

                datestring = item[0].decode('utf-8').split('-')
                date = datetime.date(int(datestring[0]), int(datestring[1]), int(datestring[2]))            
                
                cursor.execute("SELECT * from source.daily_price where id=%s AND date=%s", (code.decode('utf-8'),date))
                dp = cursor.fetchone()
                
                if dp is None:
                    if len(item)>8:
                        post = { '$set': { 'id': code.decode('utf-8') , 'date': date
                            , 'open': item[1].decode('utf-8')
                            , 'close': item[2].decode('utf-8')
                            , 'high': item[3].decode('utf-8')
                            , 'low': item[4].decode('utf-8')
                            , 'volume': item[5].decode('utf-8')
                            , 'amount': item[6].decode('utf-8')
                            , 'amplitude': item[7].decode('utf-8')
                            , 'turnover': item[8].decode('utf-8')} }
                        
                        postgres_insert_query = "INSERT INTO source.daily_price (id,date,open,close,high,low,volume,amount,turnover,amplitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        record_to_insert = (code.decode('utf-8'), date, item[1].decode('utf-8'), item[2].decode('utf-8'), item[3].decode('utf-8'), item[4].decode('utf-8'), item[5].decode('utf-8'), item[6].decode('utf-8'), item[8].decode('utf-8') ,item[7].decode('utf-8'),)
                    else:
                        post = {'$set': {'id': code.decode('utf-8'), 'date': date
                            , 'open': item[1].decode('utf-8')
                            , 'close': item[2].decode('utf-8')
                            , 'high': item[3].decode('utf-8')
                            , 'low': item[4].decode('utf-8')
                            , 'volume': item[5].decode('utf-8')
                            , 'amount': item[6].decode('utf-8')
                            , 'amplitude': item[7].decode('utf-8')
                            , 'turnover': ''}}
                    
                        postgres_insert_query = "INSERT INTO source.daily_price (id,date,open,close,high,low,volume,amount,turnover,amplitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        record_to_insert = (code.decode('utf-8'), date, item[1].decode('utf-8'), item[2].decode('utf-8'), item[3].decode('utf-8'), item[4].decode('utf-8'), item[5].decode('utf-8'), item[6].decode('utf-8'), 0 ,item[7].decode('utf-8'),)
                    #postgres_insert_query = "INSERT INTO daily_price (id,date,open,close,high,low,volume,amount,turnover,amplitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    #record_to_insert = (code.decode('utf-8'), date, item[1].decode('utf-8'), item[2].decode('utf-8'), item[3].decode('utf-8'), item[4].decode('utf-8'), item[5].decode('utf-8'), item[6].decode('utf-8'), 0 ,item[7].decode('utf-8'),)
                 
                    cursor.execute(postgres_insert_query, record_to_insert)
                    connection.commit()
                    
