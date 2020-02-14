#!/bin/bash
trap 'kill %2; kill %3; kill %4' SIGINT
cd ~/test_scoring_server
docker-compose up --build &
roslaunch mapping_server mapping_server.launch
