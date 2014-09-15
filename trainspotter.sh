#!/bin/bash

HDIR=/home/trainspotter/
ID=$RANDOM

echo "Starting trainspotter (id:$ID)" $(/bin/date) >> $HDIR/log/trainspotter-times.log
{ /usr/bin/time /usr/bin/python3 $HDIR/trainspotter/trainspotter.py 
1>$HDIR/log/trainspotter/alltrains-$(date '+%Y-%m-%d-%H-%M-%S').log 
2>>$HDIR/log/trainspotter/error.log ; } 2>&1 >>$HDIR/log/trainspotter-times.log
echo "Trainspotter stopped (id:$ID)" $(/bin/date) >> $HDIR/log/trainspotter-times.log

