#!/usr/bin/env python3

import boto3, json
from collections import OrderedDict

accounts = ["dev","prod","legacy"]

ec2Instances = {}

for account in accounts:
	print(account)
	for region in ["us-east-1", "us-west-2"]:
		print(region)
		session = boto3.Session(profile_name=account)
		client = session.client('ec2', region_name=region)


		kwargs = {}

		while True:
			response = client.describe_instances(**kwargs)
			for reservation in response["Reservations"]:
				for instance in reservation["Instances"]:
					tags =[]
					try:
						for tag in instance["Tags"]:
							tags.append({tag["Key"]:tag["Value"]})
					except:
						pass
					ec2Instances[instance["InstanceId"]] = { "Account": account, "Region": region, "Tags": tags }

			if "NextToken" not in response:
				break
			else:
				kwargs["NextToken"] = response["NextToken"]


json_string = json.dumps(ec2Instances,indent=4)

with open('ec2s.json', 'w') as outfile:
	outfile.write(json_string)
