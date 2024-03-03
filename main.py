import requests
import json
import time
import config

# Define API endpoint and station code
station = config.stationID
StationName = config.StationName
url = ("https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(station))
# Replace with your App ID
app_id = config.app_id
# Replace with your App Key
app_key = config.app_key

# Set headers with your App ID and App Key
headers = {
    "Authorization": f"Bearer {app_id}:{app_key}"
}
#function to remove duplicates
def remove_duplicates(data):
    """
    Removes duplicate entries from the JSON data based on `lineName` and `timeToStation`.
    This ensures that duplicate services are not shown seperately

    Args:
        data (list): List of dictionaries containing arrival information.

    Returns:
        list: List of dictionaries with duplicates removed.
    """
    seen = set()
    unique_data = []
    for item in data:
        key = (item["lineName"], item["timeToStation"])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
    return unique_data

# Function to display arrivals board
def display_arrivals_board(data):
    print("{} Arrivals Board:".format(StationName))
    print("-" * 100)
    print("{:<20} {:<15} {:>20}".format("Line", "Destination", "Time"))
    print("-" * 100)
    for arrival in data:
        line_name = arrival["lineName"]
        destination_name = arrival["destinationName"]
        time_to_station = arrival["timeToStation"]

        # Convert time to minutes (optional)
        minutes = int(time_to_station / 60)

        print("{:<20} {:<15} {:<10}".format(line_name, destination_name, minutes))
    print("-" * 100)

#function to strip the words "Underground Station" from the destination
def strip_destination_name(data):
    """
    Strips the string "Underground Station" from the `destinationName` field.
    This is redundant as all stops will have that text.

    Args:
        data (list): List of dictionaries containing arrival information.

    Returns:
        list: List of dictionaries with modified `destinationName` fields.
    """
    for item in data:
        destination_name = item["destinationName"]
        if destination_name.endswith(" Underground Station"):
            item["destinationName"] = destination_name[:-19]  # Remove 19 characters
    return data

#function to sort the data by timeToStation
def sort_by_time(data):
    """
    Sorts the data by `timeToStation` in ascending order.

    Args:
        data (list): List of dictionaries containing arrival information.

    Returns:
        list: List of dictionaries sorted by `timeToStation`.
    """
    return sorted(data, key=lambda x: x["timeToStation"])

#main loop begins
while True:
    # Make API request
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        data = json.loads(response.text)
        data = remove_duplicates(data)
        data = strip_destination_name(data)
        display_arrivals_board(data)
    else:
        print(f"Error: {response.status_code}")

    # Set refresh rate (in seconds)
    time.sleep(60)
