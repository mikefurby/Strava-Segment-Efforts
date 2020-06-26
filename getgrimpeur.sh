#!/bin/bash

#competition name - easily make this an arguement, but at the moment I have this script in every club folder
club="grimpeur"
#clean the ouput folder up to avoid any pre-pending of old data
rm ~/$club/output/*

#hack to re-include previously authorised users when recalling old segment effort files
cat ~/$club/input/membersdiv.csv ~/$club/input/manual_membersdiv.csv > ~/$club/input/joint_membersdiv.csv
cp ~/$club/input/joint_membersdiv.csv ~/$club/input/membersdiv.csv

#Get the Strava segment efforts for the clubname
#this could be run every time but is costly in terms of api calls, now this is replaced by webhook signalled collection
#when a new user authorises the app then a different peruser script runs to collect historical data but only if they are premium subscribers
#this routine is only needed now as a backup
#~/apps/segmentefforts.py $club

#Sort the segment efforts into divisions from the segment effort files
#this script needs reworking completely, it's a mess but it works.
~/apps/division.py $club

#Build the league tables from the division files
#also a mess but it works
~/apps/leagues.py $club

#Finalise html, remove the SSL one following SSL enableemnt of vscc-challenges.cc
#could be moved to python but the operations here are easier in bash
~/apps/finalisehtml.sh $club
~/apps/finalisehtmlssl.sh $club

#upload finished html to AWS, remove the SSL one following SSL enableemnt of vscc-challenges.cc
#could be moved to python but the operations here are easier in bash
~/apps/awsupload.sh $club
~/apps/sslawsupload.sh $club
