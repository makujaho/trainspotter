#!/bin/bash
#
# This file takes JSON dumps with train data and converts them to 
# PNG-images in the same folder as the data with heatmaps(using heatmap.py)
#

for i in $(find "${1}" -name "*.log");
do
	IMG_FILE=$(echo "$i" | sed -e 's:data:img:' -e 's:.log:.png:')
	if [ -e "$IMG_FILE" ]
	then
		echo "$IMG_FILE already exists."
	else
		echo "Converting $i to $IMG_FILE"
		python heatmap.py $i "$IMG_FILE"
	fi
done
