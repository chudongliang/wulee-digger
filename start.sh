#!/bin/bash

sleep 900

# refresh fundamental
python3 main.py > main.log

# refresh update url for missing one
python3 test.py >> main.log

sleep 3000

# refresh ticker price ,full price , min_daily
python3 backup.py >> main.log
