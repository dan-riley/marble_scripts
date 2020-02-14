#!/bin/bash
trap 'kill %1; kill %2; kill %3' SIGINT
rosrun topic_tools relay /H03/octomap_binary /octomap_binary &
rosrun topic_tools relay /pc2_out /S01/pc2_out &
rosrun octomap_pc2_converter octomap_pc2_converter
