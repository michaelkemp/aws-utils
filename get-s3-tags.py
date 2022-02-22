#!/usr/bin/env python3

import boto3, json

accounts = ["dev","prod","legacy"]

s3Buckets = {}

for account in accounts:
    print(account)
    session = boto3.Session(profile_name=account)
    accountId = session.client('sts').get_caller_identity().get('Account')
    print(accountId)

    client = session.client('s3')
    response = client.list_buckets()
    for bucket in response["Buckets"]:
        print(bucket["Name"])
        try:
            tagList = client.get_bucket_tagging( Bucket=bucket["Name"] )
        except:
            pass
        tags =[]
        try:
            for tag in tagList["TagSet"]:
                tags.append({tag["Key"]:tag["Value"]})
        except:
            pass

        s3Buckets[bucket["Name"]] = { "Account": account, "Tags": tags }
        #print(bucket["Name"])

json_string = json.dumps(s3Buckets,indent=4)

with open('s3-tags.json', 'w') as outfile:
	outfile.write(json_string)
