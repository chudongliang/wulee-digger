#!/bin/bash
nc -zvv localhost 5432 &> /dev/null
result1=$?

#Do whatever you want

if [  "$result1" != 0 ]; then
  echo  port $PORT is closed on $SERVER
  cd /Library/PostgreSQL/11/bin/
  sudo -u postgres /Library/PostgreSQL/11/bin/pg_ctl -D/Library/PostgreSQL/11/data start
  #/usr/local/bin/docker run -v ~/data:/data/db -p 27017:27017 d8b18a166eb
else
  echo port $PORT is open on $SERVER
fi
