import json
import requests
import config
import os
import time

app_key = config.app_key
app_id = config.app_id

url = "https://api.tfl.gov.uk/StopPoint/940GZZLUNFD/Arrivals"
hdr = {'Cache-Control':'no-cache'}

def convertToMinutes(seconds):
    minutes = round(seconds/60,0)
    return minutes
while true:
    try:
        r = requests.get(url, headers=hdr)
        response = r.json()
        t1 = (response[0]['timeToStation'])
        t2 = (response[1]['timeToStation'])
        t3 = (response[2]['timeToStation'])
        os.system("cls")
        print("The next train will arrive in " + str(convertToMinutes(t1)) + " minutes.")
        print("The next train will arrive in " + str(convertToMinutes(t2)) + " minutes.")
        print("The next train will arrive in " + str(convertToMinutes(t3)) + " minutes.")
        time.sleep(60)
    except Exception as e:
        print(e)