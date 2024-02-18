
import requests
import config
import os
import time

app_key = config.app_key
app_id = config.app_id
station = config.stationID

url = ("https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(station))
hdr = {'Cache-Control':'no-cache'}

def convertToMinutes(seconds):
    minutes = round(seconds/60,0)
    return minutes

def countdown(i):
    while i > 0:
        print("Refreshing in {} seconds".format(i))
        time.sleep(1)
        i -= 1
        print ("\033[A \033[A")

while True:
    try:
        r = requests.get(url, headers=hdr)
        response = r.json()
        t1 = [response[0]['towards'], (convertToMinutes(response[0]['timeToStation']))]
        t2 = [response[1]['towards'], (convertToMinutes(response[1]['timeToStation']))]
        t3 = [response[2]['towards'], (convertToMinutes(response[2]['timeToStation']))]
        t4 = [response[3]['towards'], (convertToMinutes(response[3]['timeToStation']))]
        os.system("cls")
        print("The next train towards {} will arrive in {} minutes.".format(t1[0], t1[1]))
        print("The next train towards {} will arrive in {} minutes.".format(t2[0], t2[1]))
        print("The next train towards {} will arrive in {} minutes.".format(t3[0], t3[1]))
        print("The next train towards {} will arrive in {} minutes.".format(t4[0], t4[1]))
        countdown(60)
    except Exception as e:
        print(e)