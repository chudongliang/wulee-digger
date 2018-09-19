from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import re
from pymongo import MongoClient

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)

client = MongoClient('127.0.0.1', 27017)

db = client.temporary
collection = db.price_url
db.price_url.create_index('id', unique=True)

stock = client.stock
fundamental = stock.fundamental


for v in fundamental.find({},no_cursor_timeout=True):

    query = {'id': v['id']}
    exist = collection.find_one(query)
    if not exist:
        if v['market'] == '1':
            url = 'http://quote.eastmoney.com/sh'+v['id']+'.html'
        if v['market'] == '2':
            url = 'http://quote.eastmoney.com/sz' + v['id'] + '.html'

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
            post = {'$set': {'id': v['id'] ,'url': matchUrlString}}
            query = {'id': v['id']}

            post_id = collection.update_one(query, post, True)
            print(post_id)

driver.close()

