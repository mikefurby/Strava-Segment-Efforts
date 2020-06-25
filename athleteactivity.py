import csv
import json
import requests
from sys import argv
from pprint import pprint

path=("/home/ubuntu/")

def getAccessToken(athlete_id):
    tokenFile=(path + "Strava/ycf/tokenfiles/strava_tokens.csv")
    #tokenFile=(path + "Strava/vscc/tokenfiles/strava_tokens.csv")
    access_token=""
    with open(tokenFile) as read_token_file:
        token_list = csv.DictReader(read_token_file)
        for row in token_list:
            athlete = row["id"]
            access_token = row["access_token"]
            if (athlete_id) == (athlete):
                access_token = str(row["access_token"])
                return (access_token)

def getActivitySegments(activity_list,access_token):
        headers = {"Authorization":"Bearer %s" % (access_token) }
        endpoint=("?include_all_efforts=")
        data={}
        for activity_id in activity_list:
            Endpoint = ("https://www.strava.com/api/v3/activities/" + str(activity_id) + str(endpoint))
            Download = requests.get(Endpoint,headers=headers,data=data)
            Info=json.loads(Download.text)
        #    pprint (Info)
            segment_list = []
            for segments in Info['segment_efforts']:
                segment_list.append(segments['segment']['id'])
                #print (segment_list)
                if (segments['segment']['id']) == 12128718:
                    print (segments['name'])
                    print (segments['segment']['name'])
                    print (activity_id)

def getActivities(access_token):
        headers = {"Authorization":"Bearer %s" % (access_token) }
        data={}
        Endpoint = ("https://www.strava.com/api/v3/athlete/activities")
        Download = requests.get(Endpoint,headers=headers,data=data)
        Info=json.loads(Download.text)
        #pprint (Info)
        list=[]
        for entry in Info:
            name = (entry['name'])
            id = (entry['id'])
            list.append(id)    
        print (list)
        return (list)



if __name__ == '__main__':
    script, athlete_id = argv
    access_token = getAccessToken(athlete_id)
    activities = getActivities(access_token)
    segments = getActivitySegments(activities,access_token)
