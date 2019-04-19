#!/bin/bash

echo "files = ["
cd /home/volk/txt/SRC/
for file in *.txt
do
	FILENAME=${file}
	AUTHOR=$(echo $file | awk -F- '{print $1}'| awk -F. '{print $1}')
	SOURCE=$(echo $file | awk -F- '{print $2}' | awk -F. '{print $1}')
	echo "['${AUTHOR}','${SOURCE}','/data/SRC/${FILENAME}'],"
done

echo "]"
