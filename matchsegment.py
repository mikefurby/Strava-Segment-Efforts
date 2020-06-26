#!/usr/bin/python
import csv
import json
import requests
import time
from sys import argv

script, club = argv

segmentid=20545879

path=("/home/ubuntu/")
memberlist=(path + club + "/input/membersdiv.csv")
webhook=(path + "Strava/log/webhook.log")
segmentlist=(path + club + "/segmentlist.csv")
segmentsummary=(path + club + "/input/segmentsummary.csv")
activitystream=(path + club + "/input/activity.csv")


def getdata(athleteid,access_token,f):
#this read the webhook.log and finds the unique activity ids...may not work if an activity was deleted.
    print ("before open webhook.log")
    wh = open(webhook,'r')
    lines = wh.readlines()
    print ("open webhook.log")
    activitylist = []
    for (line) in (lines):
      if str(athleteid) in (line):
        print (line)
        print (line.strip("Start:POST: (args):"))
        stripped =  (line.strip("Start:POST: (args):"))
        print (stripped)
        jsonline = json.loads(stripped)
        print str(jsonline)
        print str(jsonline["aspect_type"])
        print str(jsonline["object_id"])
        print str(jsonline["owner_id"])
        if (jsonline["object_id"]) not in activitylist:
            activitylist.append(jsonline["object_id"])
        if (jsonline["aspect_type"]) == ("delete"):
            activitylist.remove(jsonline["object_id"])
         
    wh.close()
    print (activitylist)
#time.sleep(60)

    headers = {"Authorization":"Bearer %s" % (access_token) }
    data = {}
    dataStream = {}

    #f.write(str(athleteid) + " Activity Data\n")

    for (activity) in (activitylist):
        activityEndpoint = ("https://www.strava.com/api/v3/activities/" + str(activity))
        activityGet = requests.get(activityEndpoint,headers=headers,data=data)
        activityInfo=json.loads(activityGet.text)
        #f.write("in the for loop")

        try:
            #f.write("in the try statement")
            print ("Activity ID: " + str(activityInfo["id"]))
            print ("Activity Name: " + activityInfo["name"])
            for efforts in (activityInfo["segment_efforts"]):
              if (efforts["segment"]["id"]) == segmentid:
                print (efforts["name"])
                print (efforts["elapsed_time"])
                print (efforts["segment"]["id"])
                print (efforts["segment"]["distance"])
                elev = (efforts["segment"]["elevation_high"]) - (efforts["segment"]["elevation_low"])
                f.write(str(efforts["segment"]["id"]) + ',')
                f.write(str(athleteid) + ',')
                f.write(str(activityInfo["id"]) + ',')
                f.write(str(efforts["elapsed_time"]) + ',')
                f.write(str(efforts["start_date"]) + ',')
                f.write(str(efforts["name"]) + ',')
                f.write(str(elev) + ',')
                f.write(str(efforts["kom_rank"]) + ',')
                f.write(str(efforts["pr_rank"]) + ',')
                f.write("\n")
        except:
                print ("something was excepted")
                #f.write ("something was excepted")
#f.write("\n\n")
#f.write("Activity Stream\n")
#streamEndpoint = ("https://www.strava.com/api/v3/activities/" + str(activity) + "/streams")
#streamGet = requests.get(streamEndpoint,headers=headers,data=dataStream)
#streamInfo=json.loads(streamGet.text)
#json.dump(streamInfo,f)

def initialise():
    f = open (activitystream,'w')
    members = open(memberlist,'r')
    data = csv.reader(members)
    for member in data:
        athleteid = member[0]
        access_token = member[6]
        print member
        print (athleteid,access_token)
        getdata(athleteid,access_token,f)
    f.close()
    #time.sleep(60)


if __name__ == '__main__':
    initialise()
