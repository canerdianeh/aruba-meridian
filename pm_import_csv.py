#!/usr/bin/python3

# Aruba Meridian Placemark Import from CSV
# (c) 2021 Ian Beyer
# This code is not endorsed or supported by HPE

import json
import requests
import csv
import sys

auth_token = 'Insert Access Token Here. '
location_id = 'XXXXXXXXXXXXXXXX'

baseurl = 'https://edit.meridianapps.com/api/locations/'+location_id


header_base = {'Authorization': 'Token '+auth_token}

def api_call(method,endpoint,headers,payload):
	response = requests.request(method, baseurl+endpoint, headers=headers, data=payload)
	resp_json = json.loads(response.text)
	return(resp_json)

#File name argument #1
try:
	fileName = str(sys.argv[1])
except:
	print("Exception: Enter file to use")
	exit()


# Get available maps for this location for sanity check
maps={}

# print("Available Maps: ")
for floor in api_call('GET','/maps',header_base,{})['results']:
 	maps[floor['id']] = floor['name']
# 	print (floor['name']+ ": "+ floor['id'])



import_data_file = open(fileName, 'rt')

csv_reader = csv.reader(import_data_file)
count = 0

objects = []

csv_fields = []

for line in csv_reader:
	placemark = {}

	# Check to see if this is the header row and capture field names
	if count < 1 :
		csv_fields = line
	else:
		# If this is a data row, capture the fields and put them into a dict object
		fcount = 0
		for fields in line:
			objkey = csv_fields[fcount]
			placemark[objkey] = line[fcount]
			fcount += 1

		# Add the placemark object into the object list
		objects.append(placemark)		
	count +=1

#print(json.dumps(objects, indent=2))

import_data_file.close()

#Check imported objects for create or update. If it has an ID, then update. 
for pm in objects:
	task = 'ignore'
	if pm['id'] == "" :
		task = 'create'
		print("Create new object: ")
		# Delete id from payload
		del pm['id']
	else:
		task = 'update'
		print("Update object id "+ pm['id'])


	# Remove floor from payload as it is not valid
	del pm['floor']

	# Check to see if the basics are there before making the API calls
	reject = []
	if pm['x'] == "":
		reject.append("Missing X coordinate")
	if pm['y'] == "":
		reject.append("Missing Y coordinate")
	if pm['map'] == "":
		reject.append("Missing map id")
	if pm['name'] == "":
		reject.append("Missing object name")

	if len(reject)>0:
		#print("object "+ task + " rejected due to missing required data:")
		for reason in reject:
			print(reason)
		task = 'ignore'
	else:
		if maps.get(pm['map']) == None:
			print ("Map ID "+pm['map']+" Not found in available maps. Object will not be created. ")
			task = 'ignore'
		else:
			print("object "+ task + " passed initial sanity checks and will be placed on "+ maps[pm['map']] +".")


	#print ("Object Payload:")	
	#print (json.dumps(pm, indent=2))

	method = 'GET'
	
	if task == 'create':
		#print ("Creating new object with payload:")	
		#print (json.dumps(pm, indent=2))
		method = 'POST'
		ep = '/placemarks'
		result = api_call(method,ep,header_base,pm)

		if result.get('id') != None:
			print ("Object ID "+result['id']+" named "+result['name']+ " created on map "+ result['map'])
		else:
			print ("Object not created. Errors are")
			print (json.dumps(result, indent=2))
	if task == 'update':
		#print ("Updating existing object with payload:")	
		#print (json.dumps(pm, indent=2))
		method = 'PATCH'
		ep = '/placemarks/'+pm['id']
		result = api_call(method,ep,header_base,pm)

		if result.get('id') != None:
			print ("Object ID "+result['id']+" named "+result['name']+ " updated on map "+ result['map'])
		else:
			print ("Object not updated. Errors are")
			print (json.dumps(result, indent=2))

