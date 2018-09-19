from jqdatasdk import *
from pymongo import MongoClient
auth('13917567679','cmhorse888')
from datetime import datetime

client = MongoClient("127.0.0.1",27017)
db = client.stock
min_price = db.min_price
min_price.create_index( [("id", 1), ("date", 1)], unique=True)

db = client.stock
fundamental = db.fundamental

count = 0
for v in fundamental.find({},no_cursor_timeout=True):
    count += 1;
    print(count)
    if v['market'] == '1':
        m = 'XSHG'
    if v['market'] == '2':
        m = 'XSHE'

    start = datetime(2018, 9, 12, 0, 0, 0)
    end = datetime(2018, 9, 13, 0, 0, 0)
    if not min_price.count({'id': v['id'], 'date': {'$gte' : start,'$lte' : end}}) == 240:
        print(v['id'])
        try:
            price = get_price(v['id']+'.'+m, '2018-09-12', '2018-09-13', frequency='1m', fields=None, skip_paused=True, fq='none')
            price =  price.to_dict('index')
            for i in price:
                post = {'$set': {'id': v['id'], 'date': i
                    , 'open': price[i]['open']
                    , 'close': price[i]['close']
                    , 'high': price[i]['high']
                    , 'low': price[i]['low']
                    , 'volume': price[i]['volume']
                    , 'amount': price[i]['money']}}
                query = {'id': v['id'], 'date': i}
                post_id = min_price.update_one(query, post, True)
        except Exception as e: print(e)


