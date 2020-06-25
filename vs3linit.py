#!/usr/bin/python
import csv
import json
import requests

tokenFile=("/home/ubuntu/users/strava_tokens.csv")
#appmembers=("/home/ubuntu/apps/input/membersdiv.csv")
#appmembersdetail=("/home/ubuntu/apps/input/appmembers.json")
vs3linit=("/home/ubuntu/vs3l/initfile.csv")
vs3lseglist=("/home/ubuntu/vs3l/segmentlist.csv")
clubvsccapp = 547520

#fapp = open(appmembers, 'w')
#fall = open(appmembersdetail, 'w')
finit = open(vs3linit, 'w')
fseg = open(vs3lseglist, 'w')

with open(tokenFile) as read_token_file:
  token_list = csv.reader(read_token_file, delimiter=',')
  line_count = 0
  for row in token_list:
    if line_count == 0:
      line_count += 1
    else:
      line_count += 1
      athleteid = row[0]
      athletename = row[1]
      athletetoken = row[2]
#      tokenexpiry = row[3]
#      isvs3l = row[4]
#      isgrimp = row[5]
#      error = row[6]

      print (athleteid)

      if athleteid == "46573457": 
        print(athletetoken + athletename)
        headers = {"Authorization":"Bearer %s" % (athletetoken) }
        data = {}
        athleteEndpoint = "https://www.strava.com/api/v3/athlete"
        athleteInfoDownload = requests.get(athleteEndpoint,headers=headers,data=data)
        athleteInfo=json.loads(athleteInfoDownload.text)
#        json.dump(athleteInfo, fall)
#        print(athleteInfo)
#        fall.write('\n')
        firstname=athleteInfo['firstname']
        firstname=(firstname.encode('ascii', 'ignore'))
        lastname=athleteInfo['lastname']
        lastname=(lastname.encode('ascii', 'ignore'))
        print(firstname + ',' + lastname)
        avatar=athleteInfo['profile_medium']
        athleteClubsEndpoint = "https://www.strava.com/api/v3/athlete/clubs"
        athleteClubsInfoDownload = requests.get(athleteClubsEndpoint,headers=headers,data=data)
        athleteClubsInfo=json.loads(athleteClubsInfoDownload.text)
#      json.dump(athleteClubsInfo, fall)
#      fall.write('\n')

        for clubs in athleteClubsInfo:
          eachClubId=clubs['id']
          if (eachClubId) == clubvsccapp:
#            json.dump(athleteInfo, fall)
#            fall.write('\n')
#            json.dump(athleteClubsInfo, fall)
            print (athleteClubsInfo)
#            fall.write('\n')
            athleteStarredEndpoint = "https://www.strava.com/api/v3/segments/starred"
            athleteStarredInfoDownload = requests.get(athleteStarredEndpoint,headers=headers,data=data)
            athleteStarredInfo=json.loads(athleteStarredInfoDownload.text)
#            json.dump(athleteStarredInfo, fall)
            print (athleteStarredInfo)
#            fall.write('\n')
            athleteGearEndpoint = "https://www.strava.com/api/v3/gear/b6308763"
            athleteGearInfoDownload = requests.get(athleteGearEndpoint,headers=headers,data=data)
            athleteGearInfo=json.loads(athleteGearInfoDownload.text)
#            json.dump(athleteGearInfo, fall)
            print (athleteGearInfo)
#            fall.write('\n')

            initStart=athleteGearInfo['brand_name']
            initEnd=athleteGearInfo['model_name']
            init=athleteGearInfo['description']
            print (init)
            print (initStart)
            print (initEnd)

            fseg.write("segmentid,startdate,enddate,\n")
            for segs in athleteStarredInfo:
              segment=(str(segs['id']) + ',' + str(initStart) + ',' + str(initEnd) + ',\n')
              print (segment)
              fseg.write(segment)

            finit.write(str(init) + ',\n')

fseg.close()
finit.close()
#fall.close()
