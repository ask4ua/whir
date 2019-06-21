#!/bin/bash
while true
do
    cd /data
    git stash >> /dev/null 2>&1
    /usr/bin/git clone https://gogs.ask4ua.com/root/whir-testdata.git ./ || /usr/bin/git pull
    cd /app
    python3 parser.py
    python3 decomposer.py
done