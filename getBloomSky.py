import requests
import argparse
import json
import datetime
from keen.client import KeenClient

def toMilliBar(inhg):
	return float("%.3f" % (inhg*33.86))

def toCelsius(fahrenheit):
	return float("%.3f" % ((fahrenheit-32)*0.55555))

parser = argparse.ArgumentParser(description='Take Bloomsky device data and push it to keen.io event collector')
parser.add_argument('--config', '-c', default='config.json')
args=parser.parse_args()

# Default config.json file is in the same folder.

# Read config.json
with open(args.config, 'r') as f:
	configurations = f.read()

config = json.loads(configurations)

agent_name = config["agent_name"]
project_id = config["keen.io"]["project_id"]
write_key = config["keen.io"]["write_key"]
event_collector = config["keen.io"]["event_collector"]
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
# Also below I'm doing bunch of field name normalizations to conform
# my naming standards with other IoTs that I have at home
bloomskyData[0]['Data']['temperature'] = toCelsius(bloomskyData[0]['Data']['Temperature'])
bloomskyData[0]['Data'].pop('Temperature')
bloomskyData[0]['Data']['pressure']  = toMilliBar(bloomskyData[0]['Data']['Pressure'])
bloomskyData[0]['Data'].pop('Pressure')
bloomskyData[0]['Data']['humidity'] = bloomskyData[0]['Data'].pop('Humidity')
bloomskyData[0]['Data']['agentName'] = agent_name
bloomskyData[0]['Data']['timestamp'] = datetime.datetime.utcnow().strftime("%FT%H:%M:%S.%fZ")
bloomskyData[0]['Data']['day'] = not  bloomskyData[0]['Data'].pop('Night')
bloomskyData[0]['Data']['rain'] = bloomskyData[0]['Data'].pop('Rain')
# Hoping that Electric Imp lux and BloomSky Luminance are similar :)
bloomskyData[0]['Data']['lux'] = bloomskyData[0]['Data'].pop('Luminance')

# Create the Keen.io client
client = KeenClient(
	project_id = project_id,
	write_key = write_key,
	get_timeout = 100
	)
#print bloomskyData[0]['Data']
client.add_event(event_collector, bloomskyData[0]['Data'])
