
import requests
import config
import os
import time

app_key = config.app_key
app_id = config.app_id
station = config.stationID

url = ("https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(station))
hdr = {'Cache-Control':'no-cache', 'app_id':app_id, 'app_key':app_key}

# Send request and get response
try:
  r = requests.get(url, headers=hdr)
  data = r.json()
except requests.exceptions.RequestException as e:
  print(f"Error: {e}")
  exit()
#troubleshooting data
print(data)

# Extract and display relevant information
print("Northfields Underground Station Information:")

# Display line names
print("Lines:")
for line in data["lines"]:
  print(f"- {line['name']}")

# Display platform name and destination for next arrival on each line
for line in data["lines"]:
  if line["arrivals"]:
    next_arrival = line["arrivals"][0]
    print(f"\t- Line {line['name']}: platform {next_arrival['platformName']} towards {next_arrival['destinationName']}")
  else:
    print(f"\t- Line {line['name']}: No upcoming arrivals")

# Additional information you can display (optional):
# - Station status (e.g., operational, closed)
# - Real-time departure times
# - Accessibility information

print("For more information, please visit https://www.tfl.gov.uk/underground/arrivals/")
