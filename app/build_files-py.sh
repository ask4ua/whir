#!/bin/bash

cnt=0

cd /data/SRC/
OUT="/app/files.py"
echo "files = ["

for file in *.txt;
do
	if [[ $cnt -ne 0 ]]
	then
		echo ","
	fi
	FILENAME=${file}

	AUTHOR=$(echo $file | awk -F- '{print $1}')
	SOURCE=$(echo $file | awk -F- '{print $2 $3 $4}' | awk -F. '{print $1}')

	echo -n "[\"\",\"${AUTHOR}\",\"${SOURCE}\",\"/data/SRC/${FILENAME}\"]"
	cnt=$(expr $cnt + 1)
done

echo "]"
