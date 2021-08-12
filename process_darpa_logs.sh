#!/bin/bash

# Extracts DARPA logs to a subdirectory, merges the bag file from each, then processes the topics

IFS='-'
idx=1
for file in *.tar.gz ; do
  echo "processing $file"
  read -a agents <<< "${file%.*}"
  if [ ${#agents[@]} == 7 ]; then
    dir="${agents[6]::-4}"
    if [ ${#dir} == 1 ]; then
      dir="master"
    fi
  elif [ ${#agents[@]} == 9 ]; then
    dir="${agents[8]::-4}"
  elif [ ${#agents[@]} == 10 ]; then
    dir="${agents[8]}"
  else
    dir="master"
  fi

  mkdir $dir
  mv "$file" "$dir"

  cd $dir
  echo "extracting $dir"
  tar xzf *.tar.gz
  rm *.tar.gz
  if [ "$dir" != "master" ]; then
    echo "processing bag data for $dir"
    # Reindex any active bags
    if find . -name 'robot_data_*.bag.active' -printf 1 -quit | grep -q 1; then
      for robot_active in robot_data_*.bag.active ; do
        newfile=${robot_active:0:${#robot_active}-11}
        mv "$robot_active" "$newfile.bag"
        rosbag reindex "$newfile.bag"
        rm "$newfile.orig.bag"
      done
    fi

    for robot_data in robot_data_*.bag ; do
      if [ $idx == 1 ]; then
        cp "$robot_data" ../temp_$idx.bag
      else
        let "pidx=$idx-1"
        python ~/marble/scripts/bag_utils/bagmerge.py -o ../temp_$idx.bag ../temp_$pidx.bag "$robot_data"
        rm ../temp_$pidx.bag
      fi
      let "idx=$idx+1"
    done
  fi
  find . -name '*log*' | xargs gzip
  cd ..
done

echo "moving temp bag to $name.bag"
name=${PWD##*/}
let "pidx=$idx-1"
mv temp_$pidx.bag $name.bag
echo "processing topics"
python ~/marble/scripts/bag_utils/bag_convert_ma_msgs.py $name.bag
mv $name-ma.bag $name.bag
