#!/bin/bash

filename="$HOME/base_station/base_config"

# Set via command-line
MA_NEIGHBORS="H01,H02,D01,D02"
MA_USEMESH=true
MA_INTERFACE="enp60s0"

if [ "$1" == "course" ]; then
  if [ "$2" == "local" ]; then
    # Local
    MA_SCOREADDRESS="127.0.0.1"
    MA_IPADDRESS="127.0.0.1"
    MA_SCORETOKEN="tokentokentoken1"
    MA_MAPTOKEN="FKDzKcNTugczqkpC"
    # Only set here
    if [ "$3" == "test" ]; then
      MA_TESTRELAY=true
      MA_MAPPINGRELAY=true
    else
      MA_TESTRELAY=false
      MA_MAPPINGRELAY=false
    fi
  elif [ "$2" == "1" ]; then
    # Safety Research Mine
    # Alpha Course
    MA_SCOREADDRESS="10.100.1.200"
    MA_IPADDRESS="10.100.1.201"
    MA_SCORETOKEN="zQlymxMoMtPqSMB9"
    MA_MAPTOKEN="zQlymxMoMtPqSMB9"
    MA_TESTRELAY=false
    MA_MAPPINGRELAY=true
  elif [ "$2" == "2" ]; then
    # Experimental Mine
    # Beta Course
    MA_SCOREADDRESS="10.100.2.200"
    MA_IPADDRESS="10.100.2.201"
    MA_SCORETOKEN="1JDrvQA8GUtUF22a"
    MA_MAPTOKEN="1JDrvQA8GUtUF22a"
    MA_TESTRELAY=false
    MA_MAPPINGRELAY=true
  fi
elif [ "$1" == "show" ]; then
  echo $filename
  cat $filename
  exit
elif [ "$1" == "set" ]; then
  MA_NEIGHBORS=$2
  MA_USEMESH=$3
elif [ "$1" == "wireless" ]; then
  MA_INTERFACE="wlo1"
else
  echo "usage: base_setup.sh course [local | 1 | 2] [test]"
fi

if [ "$1" ]; then
  echo "MA_NEIGHBORS=$MA_NEIGHBORS
MA_USEMESH=$MA_USEMESH
MA_INTERFACE=$MA_INTERFACE
MA_TESTRELAY=$MA_TESTRELAY
MA_MAPPINGRELAY=$MA_MAPPINGRELAY
MA_SCOREADDRESS=$MA_SCOREADDRESS
MA_IPADDRESS=$MA_IPADDRESS
MA_SCORETOKEN=$MA_SCORETOKEN
MA_MAPTOKEN=$MA_MAPTOKEN" > $filename
fi
