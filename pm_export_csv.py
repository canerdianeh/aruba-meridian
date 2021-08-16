#!/usr/bin/python3

# Aruba Meridian Placemark Export to CSV
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

placemarks=[]

for pm in (api_get('/placemarks',header_base,{}))['results']:
	pm['floor']=maps[pm['map']]
	placemarks.append(pm)

data_file = open(fileName, 'w')
csv_writer = csv.writer(data_file)
count = 0

csv_fields = ['id','floor','name','map','type','type_name','color','x','y','latitude','longitude','area','description','phone','email','url']
csv_writer.writerow(csv_fields)

#print(placemarks)
for pm in placemarks:
	data=[]
	for col in csv_fields:
		data.append(pm[col])
	# Writing data of CSV file
	csv_writer.writerow(data)
 
data_file.close()

