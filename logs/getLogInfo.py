#!/usr/bin/env python3

import boto3, json, re


conversion_log_group = '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-conversion-lambda'
traffic_log_group = '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-traffic-lambda'

LOG_PREFIX = "2022/02/10"

session = boto3.Session(profile_name="prod")
client = session.client('logs', region_name="us-east-1")

## Conversion Logs
print("\nConversion Logs\n")
all_streams = []
stream_batch = client.describe_log_streams(logGroupName=conversion_log_group, logStreamNamePrefix=LOG_PREFIX)
all_streams += stream_batch['logStreams']
while 'nextToken' in stream_batch:
	stream_batch = client.describe_log_streams(logGroupName=conversion_log_group,nextToken=stream_batch['nextToken'])
	all_streams += stream_batch['logStreams']

print(len(all_streams))

stream_names = [stream['logStreamName'] for stream in all_streams]
out_to = open("conversion_log_group.txt", 'w')
for stream in stream_names:
	print(".",end="",flush=True)
	logs_batch = client.get_log_events(logGroupName=conversion_log_group, logStreamName=stream, startFromHead=True)
	for event in logs_batch['events']:
		message = re.findall("\{(.*?)\}", event["message"])
		if len(message) == 1:
			out_to.write("{" + str(message[0]) + '}\n')
	while 'nextToken' in logs_batch:
		logs_batch = client.get_log_events(logGroupName=conversion_log_group, logStreamName=stream, nextToken=logs_batch['nextToken'])
		for event in logs_batch['events']:
			message = re.findall("\{(.*?)\}", event["message"])
			if len(message) == 1:
				out_to.write("{" + str(message[0]) + '}\n')


## Traffic Logs
print("\nTraffic Logs\n")
all_streams = []
stream_batch = client.describe_log_streams(logGroupName=traffic_log_group, logStreamNamePrefix=LOG_PREFIX)
all_streams += stream_batch['logStreams']
while 'nextToken' in stream_batch:
	stream_batch = client.describe_log_streams(logGroupName=traffic_log_group,nextToken=stream_batch['nextToken'])
	all_streams += stream_batch['logStreams']

print(len(all_streams))

stream_names = [stream['logStreamName'] for stream in all_streams]
out_to = open("traffic_log_group.txt", 'w')
for stream in stream_names:
	print(".",end="",flush=True)
	logs_batch = client.get_log_events(logGroupName=traffic_log_group, logStreamName=stream, startFromHead=True)
	for event in logs_batch['events']:
		message = re.findall("\{(.*?)\}", event["message"])
		if len(message) == 1:
			out_to.write("{" + str(message[0]) + '}\n')
	while 'nextToken' in logs_batch:
		logs_batch = client.get_log_events(logGroupName=traffic_log_group, logStreamName=stream, nextToken=logs_batch['nextToken'])
		for event in logs_batch['events']:
			message = re.findall("\{(.*?)\}", event["message"])
			if len(message) == 1:
				out_to.write("{" + str(message[0]) + '}\n')

