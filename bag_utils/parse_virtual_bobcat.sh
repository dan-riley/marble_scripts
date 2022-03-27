#!/bin/bash

echo "processing virtuals!"

for dir in *
do
  echo "processing $dir"
  cd $dir
  process_darpa_logs.sh
  python ~/marble/scripts/bag_utils/parse_bobcat.py $dir.bag X1 robot_data
  python ~/marble/scripts/bag_utils/parse_bobcat.py $dir.bag X2 robot_data
  python ~/marble/scripts/bag_utils/parse_bobcat.py $dir.bag X3 robot_data
  python ~/marble/scripts/bag_utils/parse_bobcat.py $dir.bag A01 robot_data
  python ~/marble/scripts/bag_utils/parse_bobcat.py $dir.bag A02 robot_data
  cd ..
done
