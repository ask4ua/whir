#!/bin/bash

echo "files = ["
cd /home/volk/txt/SRC/
cnt=0
for file in *.txt
do
	if [[ $cnt -ne 0 ]]
	then
		echo ","
	fi
	#FILENAME=$(echo ${file} | sed -i -e 's/\'/\\\'/g')
	FILENAME=${file}

	AUTHOR=$(echo $file | awk -F- '{print $1}'| awk -F. '{print $1}')
	SOURCE=$(echo $file | awk -F- '{print $2}' | awk -F. '{print $1}')
	echo -n "[\"${AUTHOR}\",\"${SOURCE}\",\"/data/SRC/${FILENAME}\"]"
	cnt=$(expr $cnt + 1)
done

echo "]"
