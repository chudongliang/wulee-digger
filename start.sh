#!/bin/bash

cd /Users/ChuE/wulee-digger

# refresh fundamental
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 fundamental.py 

# refresh update url for missing one
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 price_url.py 

sleep 500

# refresh ticker price ,full price , min_daily
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 backup.py 
