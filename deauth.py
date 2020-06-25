import json
import requests
from sys import argv
from pprint import pprint

class doDeauth():
    def __init__(self,access_token):
        headers = {"Authorization":"Bearer %s" % (access_token) }
        Endpoint = ("https://www.strava.com/oauth/deauthorize")
        makeRequest = requests.post(Endpoint,headers=headers)
        requestOutput=json.loads(makeRequest.text)
        pprint (requestOutput)

if __name__ == '__main__':
    script, access_token = argv
    deauth = doDeauth(access_token)
