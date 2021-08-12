#!/bin/bash

# Extracts rosout logs to a subdirectory and parses them to node files

echo "processing rosout logs"
dir="parsed"

mkdir $dir
cp rosout.log.* "$dir"

cd $dir
gzip -d *
python ~/marble/scripts/bag_utils/parse_rosout.py .
rm rosout.log*
