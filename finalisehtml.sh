#!/bin/bash
#Version 20.1

club=$1
Maxfortnights=12
NOW=$(date +"%a-%d-%B-%Y-%T")
NOW=$(date +"%c")
echo $NOW

initfilestring=~/$club/initfile.csv
######read the init file#######
while IFS=$',' read YearStr readYear SeasonStr readSeason FortStr readFortnight 
do
  Year=$readYear
  Season=$readSeason
  Fortnight=$readFortnight
done < $initfilestring
echo "done $Year $Season $Fortnight"


###Competition specific league headers###
divnames=~/$club/divnames.txt
divcount=0
while IFS=$',' read dname dhead dstartscore
do
    divcount=$((divcount+1))
    Divname[$divcount]=$dname
    Divhead[$divcount]=$dhead
done < $divnames
TotalDivs=divcount
divcount=0
while read line
do
    divcount=$((divcount+1))
    sed -i "1s|^|<h3>${Divname[$divcount]}</h3>\n ${Divhead[$divcount]}<p>|" ~/$club/output/liveleague$divcount.htm
done < $divnames




###read segment list file to count number of segments###
SEGLIST=~/$club/input/segmentsummary.csv
segc=0
while IFS="," read segment_id start_date end_date name elevation_gain kom qom
do
  segc=$((segc+1))
done <  $SEGLIST
segc=$((segc-1))
TotalSegments=$segc
echo "Number of segments: $TotalSegments"
###store the segment list in archive
cp ~/$club/segmentlist.csv ~/$club/archive/segmentlist$Year$Season$Fortnight.csv

#RECENT efforts
Counter=0
cat ~/$club/header.htm > ~/$club/html/index.html 
printf "<br>Last Updated $NOW <p><h1>Recent Efforts</h1>\n" >> ~/$club/html/index.html
while [ $Counter != $TotalSegments ]
do
  Counter=$((Counter+1))
  cat ~/$club/output/todaysefforts$Counter.htm >> ~/$club/html/index.html
done
printf "\n<img src="/icons/strava_api.png"></a></div></body>\n</html>\n" >> ~/$club/html/index.html
cp ~/$club/html/index.html ~/$club/html/index.htm

#CURRENT PERIOD TABLE
Counter=0
cat ~/$club/header.htm > ~/$club/html/current.htm
printf "<br>Last Updated $NOW <p><h1>Current Challenge Period</h1>" >> ~/$club/html/current.htm
while [ $Counter != $TotalSegments ]
do
  Counter=$((Counter+1))
  segtable=~/$club/output/segtable$Counter.htm
  cat $segtable >> ~/$club/html/current.htm
done
printf "\n<img src="/icons/strava_api.png"></a></div></body>\n</html>\n" >> ~/$club/html/current.htm
cp ~/$club/html/current.htm ~/$club/archive/current$Year$Season$Fortnight.htm


#FULL SEASON TABLE
cat ~/$club/header.htm > ~/$club/html/seasontable.htm
printf "<br>Last Updated $NOW <p><h1>Season Results</h1>" >> ~/$club/html/seasontable.htm
FortCount=0
while [ $FortCount != $Maxfortnights ]
do
  FortCount=$((FortCount+1))
  SegCounter=0
  while [ $SegCounter != $TotalSegments ]
  do
    SegCounter=$((SegCounter+1))
    cat ~/$club/archive/$Year$Season$FortCount"segtable"$SegCounter.htm >> ~/$club/html/seasontable.htm
  done
done
printf "\n<img src="/icons/strava_api.png"></a></div></body>\n</html>\n" >> ~/$club/html/seasontable.htm
cp ~/$club/html/seasontable.htm ~/$club/archive/seasontable$Year$Season.htm

#LEAGUE tables and matrices
cat ~/$club/header.htm > ~/$club/output/liveleaguehead.htm
cat ~/$club/header.htm > ~/$club/output/matrixhead.htm
printf "<br>Last Updated $NOW <p><h1>League Table</h1>" >> ~/$club/output/liveleaguehead.htm
printf "<br>Last Updated $NOW <p><h1>Completion Table</h1>" >> ~/$club/output/matrixhead.htm
count=0
printf "<img src="/icons/strava_api.png"></a></div></body></html>" > ~/$club/output/footer.htm
while [ $count != $divcount ]
do
  count=$((count+1))
  cat ~/$club/output/liveleaguehead.htm ~/$club/output/liveleague$count.htm ~/$club/output/footer.htm > temp && mv temp ~/$club/html
/liveleague$count.htm
  cat ~/$club/output/matrixhead.htm ~/$club/output/matrix$count.htm ~/$club/output/footer.htm > temp && mv temp ~/$club/html/matrix$
count.htm
done
