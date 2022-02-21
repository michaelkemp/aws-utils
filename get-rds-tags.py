#!/usr/bin/env python3

import boto3, json
from collections import OrderedDict

accounts = ["dev","prod","legacy"]

rdsInstances = {}

for account in accounts:
	print(account)
	session = boto3.Session(profile_name=account)
	accountId = session.client('sts').get_caller_identity().get('Account')
	print(accountId)

	for region in ["us-east-1", "us-west-2"]:
		print(region)
		client = session.client('rds', region_name=region)

		kwargs = {}
		while True:
			response = client.describe_db_instances(**kwargs)
			for instance in response["DBInstances"]:
				try:
					MasterUsername = instance["MasterUsername"]
				except:
					MasterUsername = ""
				try:
					DBName = instance["DBName"]
				except:
					DBName = ""
				ARN = "arn:aws:rds:{}:{}:db:{}".format(region, accountId, instance["DBInstanceIdentifier"])
				tagList = client.list_tags_for_resource( ResourceName=ARN )
				tags =[]
				try:
					for tag in tagList["TagList"]:
						tags.append({tag["Key"]:tag["Value"]})
				except:
					pass
				rdsInstances[instance["DBInstanceIdentifier"]] = { "Account": account, "Region": region, "Type": "DBInstances", "MasterUsername": MasterUsername, "DBName": DBName, "Tags": tags}

			if "Marker" not in response:
				break
			else:
				kwargs["Marker"] = response["Marker"]

		kwargs = {}
		while True:
			response = client.describe_db_clusters(**kwargs)
			for cluster in response["DBClusters"]:
				try:
					MasterUsername = cluster["MasterUsername"]
				except:
					MasterUsername = ""
				try:
					DatabaseName = cluster["DatabaseName"]
				except:
					DatabaseName = ""
				ARN = "arn:aws:rds:{}:{}:cluster:{}".format(region, accountId, cluster["DBClusterIdentifier"])
				tagList = client.list_tags_for_resource( ResourceName=ARN )
				tags =[]
				try:
					for tag in tagList["TagList"]:
						tags.append({tag["Key"]:tag["Value"]})
				except:
					pass
				rdsInstances[cluster["DBClusterIdentifier"]] = { "Account": account, "Region": region, "Type": "DBClusters", "MasterUsername": MasterUsername, "DatabaseName": DatabaseName, "Tags": tags}

			if "Marker" not in response:
				break
			else:
				kwargs["Marker"] = response["Marker"]


json_string = json.dumps(rdsInstances,indent=4)

with open('rds-tags.json', 'w') as outfile:
	outfile.write(json_string)
