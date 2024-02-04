import json
import requests
import config

app_key = config.app_key
app_id = config.app_id

url = "https://api.tfl.gov.uk/StopPoint/940GZZLUNFD/Arrivals"
hdr = {'Cache-Control':'no-cache'}
try:
    r = requests.get(url, headers=hdr)
    response = r.json()
    t1 = (response[0]['timeToStation'])
    t2 = (response[1]['timeToStation'])
    t3 = (response[2]['timeToStation'])

    print("The next train will arrive in " + str(t1) + " seconds.")
except Exception as e:
    print(e)