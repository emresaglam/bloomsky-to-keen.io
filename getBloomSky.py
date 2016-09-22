import requests
import json
import datetime
from keen.client import KeenClient

def toMilliBar(inhg):
	return "%.3f" % (inhg*33.86)

def toCelsius(fahrenheit):
	return "%.3f" % ((fahrenheit-32)*0.55555)

# Read config.json
with open('config.json', 'r') as f:
	configurations = f.read()

config = json.loads(configurations)

agent_name = config["agent_name"]
project_id = config["keen.io"]["project_id"]
write_key = config["keen.io"]["write_key"]
bloomSky_apiKey = config["bloomsky"]["api_key"]

url = "http://thirdpartyapi.appspot.com/api/skydata/"

header = {"Authorization" : bloomSky_apiKey}

r = requests.get(url, headers = header)

bloomskyData = r.json()

# Clean up the bloomsky data
bloomskyData[0]['Data'].pop('ImageURL', 0)
bloomskyData[0]['Data'].pop('TS', 0)
bloomskyData[0]['Data'].pop('ImageTS', 0)

# Convert to Celsius and millibar
bloomskyData[0]['Data']['Temperature'] = toCelsius(bloomskyData[0]['Data']['Temperature'])
bloomskyData[0]['Data']['Pressure']  = toMilliBar(bloomskyData[0]['Data']['Pressure'])
bloomskyData[0]['Data']['AgentName'] = agent_name
bloomskyData[0]['Data']['timestamp'] = datetime.datetime.utcnow().strftime("%FT%H:%M:%S.%fZ")
# Convert the bloomSky data to json
#bloomskyDataJson = json.dumps(bloomskyData[0]['Data'])

# Create the Keen.io client

client = KeenClient(
	project_id = project_id,
	write_key = write_key,
	get_timeout = 100
	)

client.add_event("bloomsky", bloomskyData[0]['Data'])
