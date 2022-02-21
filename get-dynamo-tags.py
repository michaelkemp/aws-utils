#!/usr/bin/env python3

import boto3, json
from collections import OrderedDict
from pprint import pprint


accounts = ["dev","prod","legacy"]

dynamoTables = {}

for account in accounts:
	print(account)
	session = boto3.Session(profile_name=account)
	accountId = session.client('sts').get_caller_identity().get('Account')
	print(accountId)

	for region in ["us-east-1", "us-west-2"]:
		print(region)
		client = session.client('dynamodb', region_name=region)

		kwargs = { "Limit": 10 }
		while True:
			response = client.list_tables(**kwargs)
			for table in response["TableNames"]:
				ARN = "arn:aws:dynamodb:{}:{}:table/{}".format(region, accountId, table)
				tagList = client.list_tags_of_resource( ResourceArn=ARN )
				tags =[]
				try:
					for tag in tagList["Tags"]:
						tags.append({tag["Key"]:tag["Value"]})
				except:
					pass
				dynamoTables[table] = { "Account": account, "Region": region, "Tags": tags }
			try:
				kwargs["ExclusiveStartTableName"] = response["LastEvaluatedTableName"]
			except:
				break

json_string = json.dumps(dynamoTables,indent=4)

with open('dynamodb-tags.json', 'w') as outfile:
	outfile.write(json_string)
