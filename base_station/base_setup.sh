#!/bin/bash

filename="$HOME/base_station/base_config"

# Set via command-line
MA_NEIGHBORS="H01,T02"
MA_USEMESH=true
MA_INTERFACE="enp60s0"

# Only set here
MA_TESTRELAY=false
MA_MAPPINGRELAY=false

# Local
MA_IPADDRESS="127.0.0.1"
# Safety Research Mine
# Alpha Course
#MA_IPADDRESS="10.100.1.201"
# Experimental Mine
# Beta Course
#MA_IPADDRESS="10.100.1.201"

if [ "$1" == "show" ]; then
  echo $filename
  cat $filename
  exit
elif [ "$1" == "set" ]; then
  MA_NEIGHBORS=$2
  MA_USEMESH=$3
elif [ "$1" == "wireless" ]; then
  MA_INTERFACE="wlo1"
fi

echo "MA_NEIGHBORS=$MA_NEIGHBORS
MA_USEMESH=$MA_USEMESH
MA_INTERFACE=$MA_INTERFACE
MA_TESTRELAY=$MA_TESTRELAY
MA_MAPPINGRELAY=$MA_MAPPINGRELAY
MA_IPADDRESS=$MA_IPADDRESS" > $filename
