#!/bin/bash
trap 'kill %2; kill %3; kill %4' SIGINT
roslaunch marble_common launch_multimaster.launch &
sleep 10
roslaunch marble_gui marble_gui.launch &
sleep 10
roslaunch octomap_pc2_converter merge_map.launch &
rostopic pub -r 10 /map_choice std_msgs/Int8 '{data: 7}'
