#!/bin/bash
source "$HOME/base_station/base_config"

args=""
IFS=',' read -ra ADDR <<< "$MA_NEIGHBORS"
for i in "${ADDR[@]}"; do
  args="$args $i:=true"
done

roslaunch ~/base_station/rviz.launch $args
