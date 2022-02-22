#!/usr/bin/env python3

import boto3
from datetime import datetime, timedelta
import time
import json
import re


conversion_log_group = '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-conversion-lambda'
log_group = '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-traffic-lambda'

LOG_PREFIX = "2022/02/11"

session = boto3.Session(profile_name="prod")
client = session.client('logs', region_name="us-east-1")


query = "fields @timestamp, @message" # | parse @message \"username: * ClinicID: * nodename: *\" as username, ClinicID, nodename | filter ClinicID = 7667 and username='simran+test@abc.com'"  

#log_group = '/aws/lambda/NAME_OF_YOUR_LAMBDA_FUNCTION'

start_query_response = client.start_query(
    logGroupName=log_group,
    startTime=int((datetime.today() - timedelta(hours=2)).timestamp()),
    endTime=int(datetime.now().timestamp()),
    queryString=query,
)

query_id = start_query_response['queryId']

response = None

while response == None or response['status'] == 'Running':
    print('Waiting for query to complete ...')
    time.sleep(1)
    response = client.get_query_results(
        queryId=query_id
    )
print(json.dumps(response,indent=4))
