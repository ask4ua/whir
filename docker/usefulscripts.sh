#!/usr/bin/env bash

echo password | docker secret create whir_db_password -
echo rootp@sswd | docker secret create root_db_password -
