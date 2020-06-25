#!/usr/bin/python
import csv
import json
import requests
import time
from sys import argv

script, club = argv

path=("/home/ubuntu/")
tokenFile=(path + "Strava/ycf/tokenfiles/strava_tokens.csv")
tokenFile=(path + "Strava/vscc/tokenfiles/strava_tokens.csv")
segmentlist=(path + club + "/segmentlist.csv")
segmentsummary=(path + club + "/input/segmentsummary.csv")
segmentdetail=(path + club + "/input/segmentdetail.csv")



def segment_gpx(segment_id,name,segment_stream):
    n1=name.strip()
    n2=n1.replace(" ", "")
    n3=n2.replace("'", "")
    name=n3
    gpxfile=(path + club + "/input/" + str(segment_id) + ".gpx")
    with open(gpxfile,'w') as g:
        g.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        g.write('<gpx creator="FurbyGPX" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topogr
afix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1">\n')
        g.write('<metadata>\n')
        g.write('<name>' + segname + '</name>\n')
        g.write('  <author><name>Mike Furby</name><link href="https://www.strava.com/athletes/3389967"/></author>\n')
        g.write('<copyright author="OpenStreetMap contributors"><year>2020</year><license>https://www.openstreetmap.org/copyright</l
icense></copyright>\n')
        g.write('<link href="https://www.strava.com/routes/' + str(segment_id) + '"/>\n') 
        g.write('</metadata>\n')
        g.write('<trk>\n')
        g.write('<name>' + segname + '</name>\n')
        g.write('<link href="https://www.strava.com/routes/' + str(segment_id) + '"/>\n') 
        g.write('  <type>Ride</type>\n<trkseg>\n')
        for datatype in streamInfo:
            #print (datatype["type"])
            alt_list=[]
            if (datatype["type"]) == "altitude":
                for index,alt in enumerate(datatype["data"]):
                    alt_list.append(alt)
        for datatype in streamInfo:
            #print (datatype["type"])
            if (datatype["type"]) == "latlng":
                #print (datatype["type"])
                for index,latlng in enumerate(datatype["data"]):
                    #print (str(latlng[0]) + str(index))
                    g.write('<trkpt lat="' + str(latlng[0]) + '" lon="' + str(latlng[1]) + '">')
                    g.write('<ele>' + str(alt_list[index]) + '</ele>')
                    g.write('</trkpt>\n')
                    #pass
        g.write('  </trkseg></trk></gpx>')

#need to use a valid token to get the segment info, any one will do.
athletetoken=""
print (tokenFile)
print ("\n" + "this is currently using the YCF user as that is subscribed\n")
with open(tokenFile) as read_token_file:
  token_list = csv.DictReader(read_token_file)
  for row in token_list:
      athleteid = row["id"]
      athletetoken = row["access_token"]
      if (athleteid) == "53259389":
          print ("hit:" + athleteid + ',' + row["lastname"])
          athletetoken = row["access_token"]

#now collect segment information using the token just recovered
headers = {"Authorization":"Bearer %s" % (athletetoken) }
data = {}
dataStream = {"type":"latlng","resolution":"high"}
#dataM = {"gender":"M"}
#dataF = {"gender":"F"}

fsegsumm = open(segmentsummary, 'w')
fsegsumm.write("segment_id,start_date,end_date,name,elevation,kom,qom,distance,av_grade,max_grade,climb_cat\n")
with open(segmentlist) as read_seg_file:
  seglist = csv.DictReader(read_seg_file)
  for row in seglist:
      segmentid = row['segmentid']
      segstart = row['startdate']
      segfinish = row['enddate']
      segmentstream=(path + club + "/input/" + segmentid + "_stream.csv")
      fsegstream = open(segmentstream, 'w')
      segmentEndpoint = ("https://www.strava.com/api/v3/segments/" + segmentid)
#      leaderboardEndpoint = ("https://www.strava.com/api/v3/segments/" + segmentid + "/leaderboard")
      streamEndpoint = ("https://www.strava.com/api/v3/segments/" + segmentid + "/streams")
#      print(segmentEndpoint)
#      print(leaderboardEndpoint)
      streamInfoDownload = requests.get(streamEndpoint,headers=headers,data=dataStream)
      streamInfo=json.loads(streamInfoDownload.text)
      segmentInfoDownload = requests.get(segmentEndpoint,headers=headers,data=data)
      segmentInfo=json.loads(segmentInfoDownload.text)
      json.dump(streamInfo, fsegstream)
      for datatype in streamInfo:
          print (datatype["type"])
          if (datatype["type"]) == "latlng":
              count=0
              for latlng in datatype["data"]:
                  if (count)==0:
                      print (latlng)
                      count+=1
              print (latlng)
          if (datatype["type"]) == "distance":
              count=0
              for distance in datatype["data"]:
                  if (count)==0:
                      print (distance)
                      count+=1
              print (distance)
#      json.dump(segmentInfo, fall)
#      fall.write('\n')
      segname=(segmentInfo['name'])
      segdist=(segmentInfo['distance'])
      avgrade=(segmentInfo['average_grade'])
      maxgrade=(segmentInfo['maximum_grade'])
      climbcat=(segmentInfo['climb_category'])
#      print(segname)
      segelevgain=(segmentInfo['total_elevation_gain'])
#      print(segelevgain)
      segelev=(segmentInfo['elevation_high'] - segmentInfo['elevation_low'])
#      print(segelev)
      if segelevgain < segelev:
        segelevgain = segelev
#      print(segelevgain)
#      print("let's see the leaderboard...maybe....")
      komm=1000#need to think how to do this now the leaderboard api endpoint is removed
      komf=1000
#      leaderboardInfoDownload = requests.get(leaderboardEndpoint,headers=headers,data=dataM)
#      leaderboardInfo=json.loads(leaderboardInfoDownload.text)
#      print(leaderboardInfo)
#      try:
#          komm=(leaderboardInfo['entries'][0]['elapsed_time'])
#      except:
#          komm=1000
#      print(komm)
#      leaderboardInfoDownload = requests.get(leaderboardEndpoint,headers=headers,data=dataF)
#      leaderboardInfo=json.loads(leaderboardInfoDownload.text)
#      try:
#          komf=(leaderboardInfo['entries'][0]['elapsed_time'])
#      except:
#          komf=1000
      print(segname + ',' + str(segelevgain) + ',' + str(komm) + ',' + str(komf) + ',' + str(distance))
      fsegsumm.write(segmentid + ',' + segstart + ',' + segfinish + ',')
      fsegsumm.write('"' + str(segname) + '"' + ',' + str(segelevgain) + ',')
      fsegsumm.write(str(komm) + ',' + str(komf) + ',' + str(distance) + ',')
      fsegsumm.write(str(avgrade) + ',' + str(maxgrade) + ',' + str(climbcat) + ',' + '\n')
      fsegstream.close()
      segment_gpx(segmentid,segname,streamInfo)
fsegsumm.close()
