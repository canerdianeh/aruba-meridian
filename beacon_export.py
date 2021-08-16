#!/usr/bin/python3

# Aruba Meridian Beacon Export to CSV
# (c) 2021 Ian Beyer
# https://nerdian.ca
# This code is not endorsed or supported by HPE

import json
import requests
import csv
import sys

auth_token = 'Insert Access Token Here. '
location_id = 'XXXXXXXXXXXXXXXX'

baseurl = 'https://edit.meridianapps.com/api/locations/'+location_id


header_base = {'Authorization': 'Token '+auth_token}

def api_get(endpoint,headers,payload):
	response = requests.request("GET", baseurl+endpoint, headers=headers, data=payload)
	resp_json = json.loads(response.text)
	return(resp_json)

#File name argument #1
try:
	fileName = str(sys.argv[1])
except:
	print("Exception: Enter file to use")
	exit()

maps={}

for floor in api_get('/maps',header_base,{})['results']:
	maps[floor['id']] = floor['name']

beacons=[]

# Iterate by floor for easy grouping - 
for flr in maps.keys():
	bcnlist=api_get('/beacons?map='+flr,header_base,{})
	# NOTE: If bcnlist['next'] is not null, then there are additional pages - this doesn't process those yet. 
	for bcn in bcnlist['results']:
		# Add floor name column for easier reading. 
		bcn['floor']=maps[bcn['map']]
		beacons.append(bcn)



data_file = open(fileName, 'w')
csv_writer = csv.writer(data_file)
count = 0

csv_fields = beacons[0].keys()

print(csv_fields)

csv_writer.writerow(csv_fields)

#print(placemarks)
for bcn in beacons:
	data=[]
	for col in csv_fields:
		data.append(bcn[col])
	# Writing data of CSV file
	csv_writer.writerow(data)
	count += 1
data_file.close()

print ("Exported "+str(count)+" beacons. ")

