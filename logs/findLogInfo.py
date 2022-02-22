#!/usr/bin/env python3

import boto3, json, re

LOG_PREFIX = "2022/02/14/[$LATEST]"
log_groups = ['/aws/lambda/prod-fead-sp-to-snowflake-052702658761-conversion-lambda', '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-traffic-lambda']
#log_groups = ['/aws/lambda/prod-fead-sp-to-snowflake-052702658761-traffic-lambda']


session = boto3.Session(profile_name="prod")
client = session.client('logs', region_name="us-east-1")

for log_group in log_groups:
    count = 0
    thisGroup = log_group.split("/")[-1]
    print("\n{}\n".format(thisGroup))
    all_streams = []
    stream_batch = client.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=LOG_PREFIX)
    all_streams += stream_batch['logStreams']
    print(len(all_streams))
    while 'nextToken' in stream_batch:
        stream_batch = client.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=LOG_PREFIX, nextToken=stream_batch['nextToken'])
        all_streams += stream_batch['logStreams']
        print(str(len(all_streams)) + "-")

    total = len(all_streams)
    print(total)

    stream_names = [stream['logStreamName'] for stream in all_streams]
 
    out_to = open(thisGroup + ".txt", 'w')
    upto = 0
    for stream in stream_names:
        upto += 1
        print("\n\n")
        print(str(upto) + "/" + str(total))
        print(str(count) + " -- " + stream + "\n")
        logs_batch = client.get_log_events(logGroupName=log_group, logStreamName=stream, startFromHead=True)
        for event in logs_batch['events']:
            # print(".",end="",flush=True)
            if "SubscriptionConfirmation" in event["message"]:
                print("-",end="",flush=True)
                message = re.findall("\{([\S\s]*?)\}", str(event["message"]))
                out_to.write("{" + str(message[0]) + "}\n\n")
                count += 1

        while True:
            prev_token = logs_batch['nextForwardToken']
            logs_batch = client.get_log_events(logGroupName=log_group, logStreamName=stream, nextToken=prev_token)
            # same token then break
            if logs_batch['nextForwardToken'] == prev_token:
                break
            for event in logs_batch['events']:
                # print(".",end="",flush=True)
                if "SubscriptionConfirmation" in event["message"]:
                    print("-",end="",flush=True)
                    message = re.findall("\{([\S\s]*?)\}", event["message"])
                    out_to.write("{" + str(message[0]) + "}\n\n")
                    count += 1

    print("\n\n")
    print(str(upto) + "/" + str(total))
    print(str(count) + " -- " + stream + "\n")
    out_to.close()

