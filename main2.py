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


#q=query(finance.STK_CAPITAL_CHANGE=change_reason).filter(finance.STK_CAPITAL_CHANGE.code=='600531.XSHG',finance.STK_CAPITAL_CHANGE.pub_date>'2002-01-01').limit(20)
#df=finance.run_query(q)
#print(df)

#finance.run_query(query(finance.STK_XR_XD).filter(finance.STK_XR_XD.code=='600531.XSHG').order_by(finance.STK_XR_XD.report_date).limit(20)

#q=query(finance.STK_XR_XD).filter(finance.STK_XR_XD.code=='600531.XSHG',finance.STK_XR_XD.report_date>='2002-01-01').limit(20)
#df = finance.run_query(q)
#for i in df:
#    print(df[i])
#print(df)


price = get_price('002285.XSHE', '2018-09-04', '2018-09-05', frequency='1d', fields=['open', 'close', 'factor'], skip_paused=True, fq='post')
price =  price.to_dict('index')
print(price)
