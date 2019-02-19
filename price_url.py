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

from common.db import Postgres
db = Postgres()

rows = db.fetchall("SELECT * from source.fundamental")
for v in rows:
    
    id = v[0]
    market = v[1]
    
    priceurl = db.fetchone("SELECT * from source.price_url where id=%s", (id,))
    
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
            
            postgres_insert_query = "INSERT INTO source.price_url (id,url) VALUES (%s,%s)"
            record_to_insert = (v[0], matchUrlString)
            db.insert(postgres_insert_query, record_to_insert)
               
            db.commit()

            #post_id = collection.update_one(query, post, True)
            #print(post_id)

driver.close()

