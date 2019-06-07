#!/usr/bin/env bash

docker secret rm whir_db_password >> /dev/null 2>&1 || echo "secret wasn`t exists" 
docker secret rm root_db_password >> /dev/null 2>&1 || echo "secret wasn`t exists" 

echo password | docker secret create whir_db_password -
echo rootp@sswd | docker secret create root_db_password -
