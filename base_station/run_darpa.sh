#!/bin/bash
trap 'kill %2; kill %3; kill %4' SIGINT
cd ~/test_scoring_server
docker-compose up --build &
cd ~/base_station
roslaunch mapping_server.launch
