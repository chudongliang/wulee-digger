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

db = client.temporary
collection = db.price_url

db1 = client.stock
min_price = db1.min_price
min_price.create_index( [("id", 1), ("date", 1)], unique=True)

import psycopg2

connection = psycopg2.connect(user="postgres",
                                  password="cmhorse888",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wulee")
cursor = connection.cursor()

#from data.stock.min_price import MinPrice

class MinPriceDailySpider(scrapy.Spider):

    name = 'min_price_daily_spider'

    start_urls = []
    
    cursor.execute("SELECT * from source.price_url")
    rows = cursor.fetchall()
    
    for v in rows:
        start_urls.append('http://' + v[1].replace("type=k","type=m1"))

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

                    open = float(row[1].decode('utf-8'))  
                    close = float(row[4].decode('utf-8'))
                    high = float(row[2].decode('utf-8'))
                    low = float(row[3].decode('utf-8'))
        

                    #post = {'$set': {'id': stock_id, 'date': date_time
                    #    , 'open': float(row[1].decode('utf-8'))
                    #    , 'close': float(row[4].decode('utf-8'))
                    #    , 'high': float(row[2].decode('utf-8'))
                    #    , 'low': float(row[3].decode('utf-8'))
                    #    , 'volume': float(row[6].decode('utf-8'))
                    #    , 'amount': float(row[7].decode('utf-8'))}}
                    #query = {'id': stock_id, 'date': date_time}
                    #post_id = min_price.update_one(query, post, True)
                    
                    
            
                    #print(date_time)
                    #exit()
                    cursor.execute("SELECT * from source.min_price where id=%s AND date=%s", (stock_id,date_time))
                    dp = cursor.fetchone()
                
                    if dp is None:
            
                        postgres_insert_query = "INSERT INTO source.min_price (id,date,open,close,high,low,volume,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        record_to_insert = (stock_id, date_time, open, close, high, low, float(row[6].decode('utf-8')), float(row[7].decode('utf-8')),)
                        
                      
                        cursor.execute(postgres_insert_query, record_to_insert)
                        connection.commit()
          
