#!/bin/bash

# Extracts DARPA logs to a subdirectory, merges the bag file from each, then processes the topics

IFS='-'
idx=1
for file in *.tar ; do
  echo "processing $file"
  read -a agents <<< "${file%.*}"
  if [ ${#agents[@]} == 7 ]; then
    dir="${agents[6]}"
  else
    dir="master"
  fi

  mkdir $dir
  mv "$file" "$dir"

  cd $dir
  echo "extracting $dir"
  tar xf *.tar
  rm *.tar
  if [ "$dir" != "master" ]; then
    echo "processing bag data for $dir"
    mv robot_data_0.bag.active robot_data_0.bag
    rosbag reindex robot_data_0.bag
    rm robot_data_0.orig.bag

    if [ $idx == 1 ]; then
      cp robot_data_0.bag ../temp_$idx.bag
      temp=3
    else
      let "pidx=$idx-1"
      python ~/marble/scripts/bag_utils/bagmerge.py -o ../temp_$idx.bag ../temp_$pidx.bag robot_data_0.bag
      rm ../temp_$pidx.bag
    fi
    let "idx=$idx+1"
  fi
  cd ..
done

echo "moving temp bag to $name.bag"
name=${PWD##*/}
let "pidx=$idx-1"
mv temp_$pidx.bag $name.bag
echo "processing topics"
python ~/marble/scripts/bag_utils/bag_convert_ma_msgs.py $name.bag
mv $name-ma.bag $name.bag
