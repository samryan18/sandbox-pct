# quick notebook code for getting data

from datetime import datetime, timedelta
import logging
import sys

from stravalib.client import Client

# get strava developer creds and fill out your data
ACCESS_TOKEN = "123"
MY_STRAVA_CLIENT_SECRET = "123"
MY_STRAVA_CLIENT_ID = 123

client = Client(access_token=ACCESS_TOKEN)

url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                               redirect_uri='http://127.0.0.1:5000/authorization')

# follow this url and grab the code it gives you
print(url)


# new cell
code = "GRAB THE CODE FROM THE URL REDIRECT ABOVE"
access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                              client_secret=MY_STRAVA_CLIENT_SECRET,
                                              code=code)

activity_id = 123 # any activity (you can easily get a list of recents from client)
activity = client.get_activity(activity_id).to_dict()

types = ['time', 'latlng']
stream = client.get_activity_streams(activity_id, types=types)
print(activity["type"])

shoes = activity["gear"]["name"]
elapsed_time = activity["elapsed_time"]
moving_time = activity["moving_time"]
distance_miles = activity["distance"] * 0.000621371 # meters to miles
average_heartrate = activity["average_heartrate"]
max_heartrate = activity["max_heartrate"]
start_date_local = datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%S")
name = activity["name"]
description = activity["description"]
calories = activity["calories"]

print(f"""
shoes:\t\t\t{shoes}
elapsed_time:\t\t{elapsed_time}
moving_time:\t\t{moving_time}
distance_miles:\t\t{distance_miles}
average_heartrate:\t{average_heartrate}
max_heartrate:\t\t{max_heartrate}
start_date_local:\t{start_date_local}
name:\t\t\t{name}
description:\t\t{description}
calories:\t\t{calories}
""")

# Extract latlng and time information from activity stream
latlng = stream['latlng'].data
lnglat = [[b,a] for a,b in latlng] # format for mapbox
time = stream['time'].data # not used right now

activity_details = {
    "shoes": shoes,
    "elapsed_time": elapsed_time,
    "moving_time": moving_time,
    "distance_miles": distance_miles,
    "average_heartrate": average_heartrate,
    "max_heartrate": max_heartrate,
    "start_date_local": start_date_local,
    "name": name,
    "description": description,
    "calories": calories,
    "lnglat": lnglat
}

print(
    "The size of the activity_details is "
    f"{(sys.getsizeof(activity_details)+sys.getsizeof(lnglat))/1000} kilobytes"
)
# for an all day hike from the Winds, this returned:
# The size of the activity_details is 125.568 kilobytes
# Not too bad...can down sample to 10 seconds and get to ~25KB/activity (assuming double the length of our winds trips)
# That puts us at a few MB for the whole PCT (about the same as loading an image)

# Also the data looks like this:
"""
[-120.3266510, 39.3157780],
[-120.3266430, 39.3157920],
[-120.3266310, 39.3158100],
[-120.3266190, 39.3158250],
[-120.3266070, 39.3158400],
[-120.3265930, 39.3158520],
[-120.3265810, 39.3158620],
[-120.3265680, 39.3158780],
[-120.3265550, 39.3158930],
[-120.3265390, 39.3159110],
[-120.3265270, 39.3159220],
[-120.3265180, 39.3159320],
[-120.3265090, 39.3159470],
[-120.3264990, 39.3159570],
[-120.3264860, 39.3159660],
[-120.3264760, 39.3159740],
[-120.3264650, 39.3159880],
[-120.3264540, 39.3160000],
[-120.3264430, 39.3160120],
[-120.3264300, 39.3160260],
"""
# so there's def some clever compression opportunity (will have to decrypt on the client side but that should be easy enough)
# See here:
# https://stackoverflow.com/questions/20912901/lossless-compression-for-coordinate-path-data

