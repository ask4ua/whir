#!/bin/bash
cd /data
#/usr/bin/git clone https://gogs.ask4ua.com/root/whir-testdata.git ./ || /usr/bin/git pull
/usr/bin/git clone https://gogs.ask4ua.com/root/whir-data.git --branch=eng-books ./ || /usr/bin/git pull
cd /app
python3 parser.py

while true
do
    python3 decomposer.py
done