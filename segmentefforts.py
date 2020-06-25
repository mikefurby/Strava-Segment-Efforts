#!/usr/bin/python
import csv
import json
import requests
import time
from sys import argv
from datetime import datetime

script, club = argv

rate=500
path=("/home/ubuntu/")
strava_tokens=(path + "users/strava_tokens.csv")
memberlist=(path + club + "/input/membersdiv.csv")
segmentsummary=(path + club + "/input/segmentsummary.csv")
starttime="T00:00:00Z"
endtime="T23:59:59Z"
athletetoken=""
segment_counter = 0
allefforts=(path + club + "/efforts/segmentefforts" + ".csv")
alleffortsconcise=(path + club + "/efforts/segmentefforts_concise" + ".csv")
epoch = datetime(1970,1,1)
i = datetime.utcnow()
delta_time = (i - epoch).total_seconds()
print(epoch)
print(i)
print(int(delta_time))
print("now entering the memberlist\n")
falleffortsconcise = open(alleffortsconcise, 'w')
fallefforts = open(allefforts, 'w')
falleffortsconcise.write("segment_id,athlete_id,activity_id,elapsed_time,start_date,segment_name,segment_elevation,top_10,pr,\n")

#open the club specific memberlist and read the athlete values
with open(memberlist) as read_club_memberlist:
  athlete_entry = csv.reader(read_club_memberlist, delimiter=',')
  for row in athlete_entry:
    athleteid = row[0]
    athletelastname = row[2]
    athletetoken = row[6]
    tokenexpiry = row[7]
    premium = row[11]
    expired=(int(tokenexpiry) - int(delta_time))
    print(athleteid + ',' + athletelastname + ',' + athletetoken + ',' + str(expired) + ',' + str(premium))
#now for the athlete we just read, get the segment efforts during the season so far
    if str(premium) == "True":
     with open(segmentsummary) as read_segmentsummary_file:
      segsumm = csv.DictReader(read_segmentsummary_file, delimiter=',')
      for row in segsumm:
          segment_counter += 1
          segmentid = row['segment_id']
          segstart = (row['start_date'] + starttime)
          segfinish = (row['end_date'] + endtime)
          segname = row['name']
          segelev = row['elevation']
          segkom = row['kom']
          segqom = row['qom']
          print('Debug:' + str(segment_counter) + ',' + segmentid + ',' + segstart + ',' + segfinish)
          headers = {"Authorization":"Bearer %s" % (athletetoken) }
          data = {"start_date_local":(segstart),"end_date_local":(segfinish)}        
          segmentEffortEndpoint = ("https://www.strava.com/api/v3/segments/" + segmentid + "/all_efforts")
          segmentEffortInfoDownload = requests.get(segmentEffortEndpoint,headers=headers,data=data)

#need to check that token is valid still
#I could remove this logic and just always get the latest token...but I quite like this routine
          print(segmentEffortInfoDownload.headers["status"])
          checktoken=(segmentEffortInfoDownload.headers["status"])
          if checktoken == "200 OK":
            print("ok token is still valid")
          else:
            print("need to get new token and then collect the segment effort again")
            with open(strava_tokens) as read_token_file:
              token_entry = csv.reader(read_token_file, delimiter=',')
              for row in token_entry:
                findathlete=row[0]
                newtoken=row[2]
                newexpiry=row[3]
                if findathlete == athleteid:
                  athletetoken=(newtoken)
                  expired=(int(newexpiry) - int(delta_time))
                  if (expired) < '30':
                    print("token still bad, move on for now. this should heal in a few hours")
                  else:
                    headers = {"Authorization":"Bearer %s" % (athletetoken) }
                    segmentEffortInfoDownload = requests.get(segmentEffortEndpoint,headers=headers,data=data)
                  
#########check for the strava 15 minute rate limit and sleep in 1 minute intervals
                    print(segmentEffortInfoDownload.headers)
#          print(segmentEffortInfoDownload.headers["x-ratelimit-usage"])
          ratelimitstring=(segmentEffortInfoDownload.headers["x-ratelimit-usage"])
          rate15min,rateday=(ratelimitstring.split(',',1))
          print(rate15min)
          if int(rate15min) < (rate):
            print(rate15min,". Ok, well below the 15 minute rate limit of 600")
          else:
            print(rate15min,". Reached " + str(rate) + " requests within 15 minutes. Sleeping for 60seconds, repeat until the 15 min
ute rate resets to 0")
            time.sleep(60)


#finally print the entire segment effort info to the concise file
          segmentEffortInfo=json.loads(segmentEffortInfoDownload.text)
          fallefforts.write(str(segmentEffortInfo))
          fallefforts.write('\n')
          for efforts in segmentEffortInfo:
            print (efforts)
            try:
                komrank=(efforts['kom_rank'])
                prrank=(efforts['pr_rank'])
                segname=(efforts['name'])
                athleteid=(efforts['athlete']['id'])
                activityid=(efforts['activity']['id'])
                segid=(efforts['segment']['id'])
                elapsedtime=(efforts['elapsed_time'])
                date=(efforts['start_date'])
                print(str(athleteid) + ',' + str(activityid) + ',' + str(elapsedtime) + ',' + str(date) + ',' + segname + ',' + str(
komrank) + ',' + str(prrank))
                falleffortsconcise.write(str(segid))
                falleffortsconcise.write(',' + str(athleteid))
                falleffortsconcise.write(',' + str(activityid))
                falleffortsconcise.write(',' + str(elapsedtime))
                falleffortsconcise.write(',' + str(date))
                falleffortsconcise.write(',"' + segname + '"')
                falleffortsconcise.write(',' + segelev)
                falleffortsconcise.write(',' + str(komrank))
                falleffortsconcise.write(',' + str(prrank))
                falleffortsconcise.write('\n')
            except:
                pass
falleffortsconcise.close()
