#!/bin/bash
#
# This file takes JSON dumps with train data in data/ and converts them to 
# PNG-images in img/ with heatmaps(using heatmap.py)
#

test -d ../img || mkdir ../img

for i in ../data/alltrains-*
do
	IMG_FILE=$(echo "$i" | sed -e 's:data:img:' -e 's:.log:.png:')
	if [ -e "$IMG_FILE" ]
	then
		echo "$IMG_FILE already exists."
	else
		echo "Converting $i to image"
		python heatmap.py $i "$IMG_FILE"
	fi
done
