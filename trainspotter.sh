#!/bin/bash

HDIR=/home/trainspotter/
ID=$RANDOM

FOLDER=/home/trainspotter/log/trainspotter/trainlog-$(date '+%Y')/$(date '+%m')/$(date '+%d')
DATE=$(date '+%Y-%m-%d-%H-%M-%S')

echo "Starting trainspotter (id:$ID)" $(/bin/date) >> $HDIR/log/trainspotter-times.log
mkdir -p $FOLDER
{ \
	/usr/bin/time /usr/bin/python3 /home/trainspotter/trainspotter/trainspotter.py \
		1>$FOLDER/alltrains-$DATE.log \
	2>>/home/trainspotter/log/trainspotter/error.log ; \
} 2>&1 >>/home/trainspotter/log/trainspotter-times.log
echo "Trainspotter stopped (id:$ID)" $(/bin/date) >> $HDIR/log/trainspotter-times.log

cd /home/trainspotter/trainspotter/
./import_to_es.py $FOLDER
