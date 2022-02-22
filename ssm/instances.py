#!/usr/bin/env python3

import boto3, json, re

PROFILE = "legacy"
REGION = "us-east-1"
BUCKET = "kempy-ssm-output-613196291743"

session = boto3.Session(profile_name=PROFILE)
client = session.client('ec2', region_name=REGION)

response = client.describe_instances()

kwargs = { 
    "MaxResults" : 10
}

print("#!/bin/bash\n")

print("aws s3 rm s3://{} --recursive --profile {} --region {}".format(BUCKET,PROFILE, REGION))

while (True):
    response = client.describe_instances(**kwargs)
    for Reservation in response["Reservations"]:
        for Instance in Reservation["Instances"]:
            name = ""
            inst = ""
            exIP = ""
            inIP = ""
            stat = ""

            stat = Instance["State"]["Name"]
            inst = Instance["InstanceId"]

            for tag in Instance["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]
            try:
               exIP = Instance["PublicIpAddress"]
            except:
                exIP = "0.0.0.0"
            try:
                inIP = Instance["PrivateIpAddress"]
            except:
                inIP = "0.0.0.0"
            
            if stat == "running":
                print("\n# {} {} {}".format(name, inIP, exIP))
                print("# aws ssm start-session --target {} --profile {} --region {}".format(inst, PROFILE, REGION))
                print("aws ssm send-command \\")
                print("    --targets \"Key=instanceids,Values={}\" \\".format(inst))
                print("    --document-name \"AWS-RunShellScript\" \\")
                print("    --parameters 'commands=[\"find /home/ec2-user/ -name \\\".env\\\" -exec cat {} \\;\"]' \\")
                print("    --output-s3-bucket-name {} \\".format(BUCKET))
                print("    --output-s3-key-prefix {} \\".format(name.replace(" ","_")))
                print("    --comment \"cat .env file\" \\")
                print("    --profile {} --region {} > /dev/null 2>&1".format(PROFILE, REGION))

    if 'NextToken' not in response:
        break
    else:
        kwargs['NextToken'] = response["NextToken"]

print("mkdir -p outputs")
print("aws s3 cp s3://{} outputs --recursive --profile {} --region {}".format(BUCKET,PROFILE, REGION))