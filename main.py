import requests
import json
import time
import config

# Define API endpoint and station code
station = config.stationID
url = ("https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(station))
# Replace with your App ID
app_id = config.app_id
# Replace with your App Key
app_key = config.app_key

# Set headers with your App ID and App Key
headers = {
    "Authorization": f"Bearer {app_id}:{app_key}"
}

# Function to display arrivals board
def display_arrivals_board(data):
    print("Northfields Arrivals Board:")
    print("-" * 100)
    print("{:<20} {:<15} {:<10}".format("Line", "Destination", "Time"))
    print("-" * 100)
    for arrival in data:
        line_name = arrival["lineName"]
        destination_name = arrival["destinationName"]
        time_to_station = arrival["timeToStation"]

        # Convert time to minutes (optional)
        minutes = int(time_to_station / 60)

        print("{:<20} {:<15} {:<10}".format(line_name, destination_name, minutes))
    print("-" * 100)


while True:
    # Make API request
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        data = json.loads(response.text)
        display_arrivals_board(data)
    else:
        print(f"Error: {response.status_code}")

    # Set refresh rate (in seconds)
    time.sleep(60)
