#!/usr/bin/env python3

import boto3, json
from collections import OrderedDict

accounts = ["dev","prod","legacy"]

keyValues = {}

for account in accounts:
	print(account)
	session = boto3.Session(profile_name=account)
	client = session.client('resourcegroupstaggingapi')


	keys = []
	page = ""

	while True:
		print(".",end="",flush=True)
		response = client.get_tag_keys(PaginationToken=page)
		keys += response["TagKeys"]
		page = response["PaginationToken"]
		if page == "":
			break

	#print(keys)


	for key in keys:
		print(".")
		if key.startswith("aws:"):
			continue
		if key == "Name":
			continue

		#print("KEY: {}".format(key))
		page = ""
		values = []
		while True:
			print(".",end="",flush=True)
			response = client.get_tag_values(PaginationToken=page, Key=key)
			values += response["TagValues"]
			page = response["PaginationToken"]

			if page == "":
				break

		try:
			keyValues[key] += values
		except:
			keyValues[key] = values

for key in keyValues:
	keyValues[key] = list(set(keyValues[key]))


json_string = json.dumps(keyValues,indent=4)

with open('tags.json', 'w') as outfile:
	outfile.write(json_string)
