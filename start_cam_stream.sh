#!/bin/bash

gpspath="/dev/ttyACM0"
token=""


while getopts "gp:l:t" opt
do
  case "${opt}" in
    g) gpspath="${OPTARG}";;
    p) projectid="${OPTARG}";;
    l) pwrlinename="${OPTARG}";;
    t) token="${OPTARG}";;
    u) ubirdurl="${OPTARG}";;
  esac
done

echo "$gpspath";
echo "$projectid"
echo "$pwrlinename"
echo "$token"
echo "$ubirdurl"

cd /home/pi/Camera_CLI
python3 camera.py -g $gpspath -p $projectid -l $pwrlinename -t $token -u $ubirdurl
