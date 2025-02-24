import requests
import json
import time
import config
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer


# Define API endpoint and station code
station = config.stationID
StationName = config.StationName
url = "https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(station)
# Replace with your App ID
app_id = config.app_id
# Replace with your App Key
app_key = config.app_key


# Set headers with your App ID and App Key
headers = {"Authorization": f"Bearer {app_id}:{app_key}"}


# function to remove duplicates
def remove_duplicates(data):
    """
    Removes duplicate entries from the JSON data based on `lineName`
    and `timeToStation`.
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


# function to strip the words "Underground Station" from the destination
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
        destination_name = item.get("destinationName", "")
        if destination_name.endswith(" Underground Station"):
            item["destinationName"] = destination_name[:-19]
    return data


# function to sort the data by timeToStation
def sort_by_time(data):
    """
    Sorts the data by `timeToStation` in ascending order.

    Args:
        data (list): List of dictionaries containing arrival information.

    Returns:
        list: List of dictionaries sorted by `timeToStation`.
    """
    return sorted(data, key=lambda x: x["timeToStation"])


def fetch_arrival_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = sort_by_time(data)
        data = strip_destination_name(data)
        data = remove_duplicates(data)
        return data
    else:
        print(f"Error: {response.status_code}")
        return []
    
# PyQt5 application
class TubeStationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tube Station Information')
        self.setGeometry(100, 100, 300, 300)

        #set the background color to black and the text to yellow
        self.setStyleSheet("background-color: black; color: yellow;")

        layout = QVBoxLayout()

        self.arrivals_label = QLabel('Gloucester Road:')
        layout.addWidget(self.arrivals_label)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.refresh_data()

        # Set up the timer to auto-refresh every 60 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(60000)  # 60 seconds

    def refresh_data(self):
        arrival_data = fetch_arrival_data()
        self.display_arrivals(arrival_data)

    def display_arrivals(self, data):
        # Clear the grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add headers
        self.grid_layout.addWidget(QLabel("Line"), 0, 0)
        self.grid_layout.addWidget(QLabel("Destination"), 0, 1)
        self.grid_layout.addWidget(QLabel("Time"), 0, 2)

        # Add data points
        for row, arrival in enumerate(data, start=1):
            line_name = arrival.get("lineName", "Unknown")
            destination_name = arrival.get("destinationName", "Check Front of Train")
            time_to_station = arrival.get("timeToStation", 0)
            minutes = int(time_to_station / 60)

            self.grid_layout.addWidget(QLabel(line_name), row, 0)
            self.grid_layout.addWidget(QLabel(destination_name), row, 1)
            self.grid_layout.addWidget(QLabel(str(minutes)), row, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TubeStationApp()
    ex.show()
    sys.exit(app.exec_())