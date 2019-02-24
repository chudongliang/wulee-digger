# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
import psycopg2

from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast
import sys

from common.db import Postgres

db = Postgres()

class FunSpider(scrapy.Spider):
    name = 'fun_spider'
    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=&sortRule=-1&page=2&pageSize=20&js=var%20uBbVOftU={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517353374426']

    def parse(self, response):
        if b'pages' in response.body:
            s = response.body.split(b'rank:[\"')
            s = s.pop()

            items = s.split(b'\",\"')
            for k in items:
                item = k.split(b',')
                print(item[1].decode('utf-8'))
                print(item[2].decode('utf-8'))
                
                postgres_insert_query = "INSERT INTO source.fundamental VALUES (%s,%s,%s) ON CONFLICT (id) DO UPDATE SET name = %s"

                record_to_insert = (item[1].decode('utf-8'), item[0].decode('utf-8'), item[2].decode('utf-8'), item[2].decode('utf-8'))
                db.insert(postgres_insert_query, record_to_insert)
               
            db.commit()
            count = db.cur.rowcount
            print (count, "Record inserted successfully into fundamental table")