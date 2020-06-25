import csv
import json
import argparse
import datetime

segsummall="/home/ubuntu/grimpeur/input/segmentsummary.csv"
g2016="/home/ubuntu/grimpeur/segmentlist2016.csv"
g2017="/home/ubuntu/grimpeur/segmentlist2017.csv"
g2018="/home/ubuntu/grimpeur/segmentlist2018.csv"
g2019="/home/ubuntu/grimpeur/segmentlist2019.csv"
g2020="/home/ubuntu/grimpeur/segmentlist2020.csv"
allsegs="/home/ubuntu/grimpeur/maps/allsegments.html"
htmhead="/home/ubuntu/grimpeur/header.htm"

def segyears(segs):
    seglist = []
    with open(segs) as s:
        segments=csv.reader(s)
        for segment in segments:
            segment_id=segment[0]
            seglist.append(segment_id)
    print (seglist)
    return seglist

def main():
    seglist2016=segyears(g2016)
    seglist2017=segyears(g2017)
    seglist2018=segyears(g2018)
    seglist2019=segyears(g2019)
    allseglist=[]

    with open(allsegs,'w') as alls:
#      alls.write('<!DOCTYPE html><html><head>')
#      alls.write('<style>table, th, td {  border: 1px solid black;border-spacing: 5px;}</style>')
#      alls.write('</head><body>')
      with open(htmhead) as hh:
          lines=hh.readlines()
          for line in lines:
              alls.write(line)
      alls.write('<h1>Grimpeur Hill Climbs</h1>')
      alls.write('<table border="1" width="100%"><tr> <th>Segment Name</th> <th>Links</th> <th>Featured in</th> <th>Segment Data</th
> <th>Ascents</th> </tr>')
      with open(segsummall) as s:
        segments=csv.DictReader(s)
        unique=0
        for count,segment in enumerate(segments,start=1):
          segment_id=(segment["segment_id"])
          with open("/home/ubuntu/grimpeur/efforts/4yeararchive/segmentefforts_concise_" + str(count) + '.csv') as efforts:
                    effortlist=csv.reader(efforts)
                    for effcount,effort in enumerate(effortlist):
                       pass
          if (segment_id) not in (allseglist):
            unique+=1
            allseglist.append(segment_id)
            segment_name=(segment["name"])
            segfile=("/home/ubuntu/grimpeur/input/" + str(segment_id) + ".htm")
            html_lines=[]
            html_lines.append('<tr>')
            html_lines.append('<td>' + str(unique) + ' ' + segment_name +'</td>')
            html_lines.append('<td><a href="https://www.strava.com/segments/' + segment_id + '">Strava</a> ')
            html_lines.append('<a href="https://veloviewer.com/segment/' + segment_id + '">Veloviewer</a>')
            html_lines.append('<a href="/gpx/' + segment_id + '.gpx">GPX</a></td>')
            html_lines.append('<td>')
            if (segment_id) in (seglist2016):
                    html_lines.append('2016 ')             
            if (segment_id) in (seglist2017):
                    html_lines.append('2017 ')               
            if (segment_id) in (seglist2018):
                    html_lines.append('2018 ')               
            if (segment_id) in (seglist2019):
                    html_lines.append('2019 ')               
            html_lines.append('</td>')
            komtime=str(datetime.timedelta(seconds=int(segment["kom"])))
            qomtime=str(datetime.timedelta(seconds=int(segment["qom"])))
            html_lines.append('<td>')
            #html_lines.append('KOM: ' + komtime)
            #html_lines.append(' QOM: ' + qomtime)
            html_lines.append('Elevation: ' + (segment["elevation"]) + ' meters')
            html_lines.append(' Distance: ' + (segment["distance"]) + ' meters')
            html_lines.append(' Average Grade: ' + (segment["av_grade"]) + '%')
            html_lines.append(' Maximum Grade: ' + (segment["max_grade"] + '%'))
            html_lines.append(' Climb Category: ' + (segment["climb_cat"]))
            html_lines.append('</td>')
            html_lines.append('<td>' + str(effcount) + '</td>')
            #print (html_lines)
            with open (segfile,'w') as sf:
                for line in (html_lines):
                    #print (line)
                    alls.write(line+'\n')
                    sf.write(line+'\n')
            alls.write('</tr>')
      alls.write('</table></body>')
    print(allseglist)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--club", required=True,
        help="Club name")
    args = vars(ap.parse_args())
    club_arg = (args['club'])
    main()
