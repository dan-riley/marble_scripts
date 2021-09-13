#!/bin/bash
source "$HOME/base_station/base_config"

testrelay=false
if [ "$1" == "test" ]; then
  testrelay=true
fi
roslaunch ~/base_station/darpa_comms_test.launch robots:=$MA_NEIGHBORS mapAddress:=$MA_IPADDRESS mapToken:=$MA_MAPTOKEN scoreAddress:=$MA_SCOREADDRESS scoreToken:=$MA_SCORETOKEN testRelay:=$testrelay
