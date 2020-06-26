import csv
import json
import requests
from sys import argv
from pprint import pprint

def get_token():
#need to use a valid token to get the segment info, any one will do.
    path=("/home/ubuntu/")
    tokenFile=(path + "Strava/ycf/tokenfiles/strava_tokens.csv")
    #tokenFile=(path + "Strava/vscc/tokenfiles/strava_tokens.csv")
    access_token=""
    with open(tokenFile) as read_token_file:
        token_list = csv.DictReader(read_token_file)
        for row in token_list:
            athlete_id = row["id"]
            access_token = row["access_token"]
            if (athlete_id) == "53259389":
                access_token = str(row["access_token"])
                return (access_token)

def endpoint_query(segment_id,data,endpoint):
        access_token = get_token()
        headers = {"Authorization":"Bearer %s" % (access_token) }
        segmentEndpoint = ("https://www.strava.com/api/v3/segments/" + str(segment_id) + str(endpoint))
        segmentInfoDownload = requests.get(segmentEndpoint,headers=headers,data=data)
        segmentInfo=json.loads(segmentInfoDownload.text)
        pprint (segmentInfo)

def activity_endpoint_query(activity_id,data,endpoint,access_token):
        #access_token = get_token()
        headers = {"Authorization":"Bearer %s" % (access_token) }
        segmentEndpoint = ("https://www.strava.com/api/v3/activities/" + str(activity_id) + str(endpoint))
        segmentInfoDownload = requests.get(segmentEndpoint,headers=headers,data=data)
        segmentInfo=json.loads(segmentInfoDownload.text)
        pprint (segmentInfo)
        segment_list = []
        for segments in segmentInfo['segment_efforts']:
            #print (segments['segment_efforts'])
            print (segments['name'])
            segment_list.append(segments['segment']['id'])
        print (segmentEndpoint)
        print (segment_list)

class getActivitySegments():
    def __init__(self,activity_id,access_token):
        endpoint=("?include_all_efforts=")
        #endpoint=("")
        data ={} 
        activity = activity_endpoint_query(activity_id,data,endpoint,access_token)

class getSegment():
    def __init__(self,segment_id):
        endpoint=("")
        data = {}
        segment = endpoint_query(segment_id,data,endpoint)

class getSegmentStreams():
    def __init__(self,segment_id):
        endpoint=("")
        data = {}
        streams = endpoint_query(segment_id,data,endpoint)

class getKom():
    def __init__(self,segment_id):
        endpoint=("/leaderboard")
        data = {"gender":"M"}
        komtime = endpoint_query(segment_id,data,endpoint)

class getQom():
    def __init__(self,segment_id):
        endpoint=("/leaderboard")
        data = {"gender":"F"}
        qomtime = endpoint_query(segment_id,data,endpoint)

if __name__ == '__main__':
    script, object_id = argv
    access_token="f9a0f2ca00f487e09dff346bf5559e304dcb55bd"
    #segment_data = getSegment(object_id)
    #segment_streams = getSegmentStreams(object_id)
    #kom = getKom(object_id)
    #qom = getQom(object_id)
    activity = getActivitySegments(object_id,access_token)
