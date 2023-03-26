import requests
import json
import pandas as pd
from datetime import datetime
import time

while True:
    # Define the API endpoint
    url = "https://data.traffic.hereapi.com/v7/flow"

    # Define the query parameters
    params = {
        "locationReferencing": "shape",
        #"in": "bbox:107.54908372065572,-6.926620456605005,107.72967148820469,-6.896286771555365"
        "in": "bbox:107.2510292754,-7.3097642655,107.9384321719,-6.8128449268",
        "apiKey": "z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c",
        "responseattributes": "sh,fc"
    }

    # Send the HTTP GET request to the API endpoint and get the response
    response = requests.get(url, params=params)

    # Extract the JSON data from the response
    data = json.loads(response.text)

    # Get the current timestamp in UTC
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # Save the JSON data to a file with the timestamp in the filename
    with open(f"{timestamp}.json", "w") as f:
        json.dump(data, f)

    # Wait for 30 minutes before repeating the loop
    time.sleep(120)
