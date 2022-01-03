from datetime import datetime, timedelta
import logging
import sys

from stravalib.client import Client

# get strava developer creds and fill out your data
ACCESS_TOKEN = "xyz"
MY_STRAVA_CLIENT_SECRET = "xyz"
MY_STRAVA_CLIENT_ID = 123

client = Client(access_token=ACCESS_TOKEN)

url = client.authorization_url(
    client_id=MY_STRAVA_CLIENT_ID,
    redirect_uri='http://localhost:8888/authorized',
    scope='activity:read_all'
)


# follow this url and grab the code it gives you
print(url)


# new cell
code = "205050c15b270c7bc403f1da80d7ff8ad55727cb"
access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                              client_secret=MY_STRAVA_CLIENT_SECRET,
                                              code=code)
start_date = datetime.strptime("04/20/2021", "%m/%d/%Y")
end_date = datetime.strptime("08/24/2021", "%m/%d/%Y")

activities = client.get_activities(before=end_date, after=start_date)
activities = [a for a in activities if a.type=="Hike"]

from tqdm.notebook import tqdm
import warnings
warnings.filterwarnings("ignore")
activity_details = []

for a in tqdm(activities):
    activity = client.get_activity(a.id).to_dict()

    types = ['time', 'latlng']
    stream = client.get_activity_streams(a.id, types=types)
    
    # Extract latlng and time information from activity stream
    latlng = stream['latlng'].data
    lnglat = [[b,a] for a,b in latlng] # format for mapbox
    time = stream['time'].data # not used right now

    activity_details.append({
        "elapsed_time": activity["elapsed_time"],
        "pace": activity["average_speed"]*26.8224,
        "moving_time": activity["moving_time"],
        "distance_miles": activity["distance"] * 0.000621371, # meters to miles,
        "average_heartrate": activity["average_heartrate"],
        "max_heartrate": activity["max_heartrate"],
        "start_date_local": str(datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%S")),
        "name": activity["name"],
        "shoes": activity["gear"]["name"],
        "vert_feet": activity["total_elevation_gain"]*3.28084, # meters to feet
        "description": activity["description"],
        "calories": activity["calories"],
        "lnglat": lnglat[::5] # every 5 measurements (seconds)
    })

print(
    "The size of the activity_details is "
    f"{(sys.getsizeof(activity_details)+sys.getsizeof(lnglat))/1000} kilobytes"
)

with open("data.js", "w") as file1:
    file1.write(f"let coordinates ={str(activity_details)}")
