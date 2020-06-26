#!/bin/bash
#Version 20.1

club=$1

#UPLOAD
mkdir ~/$club
mkdir ~/$club/archive
mkdir ~/$club/efforts
mkdir ~/$club/efforts/riders
mkdir ~/$club/html
mkdir ~/$club/input
mkdir ~/$club/input/gpx
mkdir ~/$club/maps
mkdir ~/$club/output
mkdir ~/Strava/$club/efforts
mkdir ~/Strava/$club/tokenfiles
mkdir ~/Strava/$club/tokenfiles/archive

printf """
Division1,Div header text,10,v,y,
Division2,Top 3 will be promoted bottom 3 will be relegated,10,v,y,
Division3,Top 3 will be promoted,10,v,y,
Division4,Top 3 will be promoted,10,v,y,
Ladies,,10,v,y,
V40-49,Please let Mike know if you want to be in this category,10,v,y,
V50-V99,Please let Mike know if you want to be in this category,10,v,y,
Everyone: Graded Handicap,,20,v,y,
Gents,,10,v,y,
KOMscore,,0,g,y
QOMscore,,0,g,y
""" > ~/$club/divnames.txt

cp ~/vscctt/header.htm ~/$club/

printf "Year,2020,Season,1,Fortnight,1,\n" > ~/$club/initfile.csv

printf "segmentid,startdate,enddate,\n" > ~/$club/segmentlist.csv
printf "14290673,2010-01-01,2020-12-31,\n" > ~/$club/segmentlist.csv


#THE ENDc
