from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import re
from pymongo import MongoClient
import psycopg2

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)

## TODO: probably die for the timeout issue
driver.set_page_load_timeout(600)


connection = psycopg2.connect(user="postgres",
                                  password="cmhorse888",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="stock")
cursor = connection.cursor()

client = MongoClient('127.0.0.1', 27017)

db = client.temporary
collection = db.price_url
db.price_url.create_index('id', unique=True)

stock = client.stock
fundamental = stock.fundamental

#sql = "SELECT * from public.fundamental"
cursor.execute("SELECT * from public.fundamental")
rows = cursor.fetchall()

for v in rows:
    
    id = v[0]
    market = v[1]
    
    cursor.execute("SELECT * from public.price_url where id=%s", (id,))
    priceurl = cursor.fetchone()
    
    if priceurl is None:
        if market == '1':
            url = 'http://quote.eastmoney.com/sh'+id+'.html'
        if market == '2':
            url = 'http://quote.eastmoney.com/sz' +id+ '.html'

        driver.get(url)
            
        matchUrlString = ""
        for entry in driver.get_log('performance'):

            if 'eastmoney.com/EM_UBG_PDTI_Fast' in json.dumps(entry):
                matchUrl = re.search(r'pdfm.eastmoney.com\/EM_UBG_PDTI_Fast(.*?)\"', json.dumps(entry), re.I | re.S | re.M)
                if 'authorityType' in matchUrl.group():
                    matchUrlString = matchUrl.group()[:-2]
                    break

        if matchUrlString:
            print(matchUrlString)
            #post = {'$set': {'id': v['id'] ,'url': matchUrlString}}
            #query = {'id': v['id']}
            
            postgres_insert_query = "INSERT INTO price_url VALUES (%s,%s)"

            record_to_insert = (id, matchUrlString)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount

            #post_id = collection.update_one(query, post, True)
            #print(post_id)

driver.close()

