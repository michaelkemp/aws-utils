#!/usr/bin/env python3

import boto3, json, re

regions = ["us-west-2", "us-east-1", "ap-south-1"]
profiles = ["dev", "prod", "legacy"]

str = "Account,Region,DBType,Identifier,MultiAZ,Class,Engine,EngineVersion,EngineMode\n"

for profile in profiles:
  session = boto3.Session(profile_name=profile)
  for region in regions:
    client = session.client('rds', region_name=region)
    paginator = client.get_paginator('describe_db_instances').paginate()
    for page in paginator:
      for dbinstance in page['DBInstances']:
        try:
          EngineMode = dbinstance["EngineMode"]
        except:
          EngineMode = ""
        str = str + "{},{},{},{},{},{},{},{},{}\n".format(
          profile, region, "Instance", dbinstance["DBInstanceIdentifier"], 
          dbinstance["MultiAZ"], dbinstance["DBInstanceClass"], dbinstance["Engine"], 
          dbinstance["EngineVersion"], EngineMode)


    paginator = client.get_paginator('describe_db_clusters').paginate()
    for page in paginator:
      for dbcluster in page['DBClusters']:
        try:
          EngineMode = dbcluster["EngineMode"]
        except:
          EngineMode = ""
        try:
          DBClusterInstanceClass = dbinstance["DBClusterInstanceClass"]
        except:
          DBClusterInstanceClass = "aurora"
        str = str + "{},{},{},{},{},{},{},{},{}\n".format(
          profile, region, "Cluster", dbcluster["DBClusterIdentifier"], 
          dbcluster["MultiAZ"], DBClusterInstanceClass, dbcluster["Engine"], 
          dbcluster["EngineVersion"], EngineMode)

print(str)
