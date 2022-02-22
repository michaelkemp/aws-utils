#!/usr/bin/env python3

import boto3
import json
import random


READ_CONV = "FEAD-Sp-Conversion-Queue"
READ_TRAF = "FEAD-Sp-Traffic-Queue"
READ_SESSION = boto3.Session(profile_name="prod")
READ_SQS = READ_SESSION.client("sqs", region_name="us-east-1")
READ_CONV_URL = READ_SQS.get_queue_url(QueueName=READ_CONV).get('QueueUrl')
READ_TRAF_URL = READ_SQS.get_queue_url(QueueName=READ_TRAF).get('QueueUrl')

WRITE_CONV = "Sp-Conversion"
WRITE_TRAF = "Sp-Traffic"
WRITE_SESSION = boto3.Session(profile_name="dev")
WRITE_SQS = WRITE_SESSION.client("sqs", region_name="us-east-1")
WRITE_CONV_URL = WRITE_SQS.get_queue_url(QueueName=WRITE_CONV).get('QueueUrl')
WRITE_TRAF_URL = WRITE_SQS.get_queue_url(QueueName=WRITE_TRAF).get('QueueUrl')

def getMessages(SQS, qURL):
    resp = SQS.receive_message(QueueUrl=qURL, AttributeNames=['All'], MaxNumberOfMessages=10, VisibilityTimeout=30)
    messages = []
    try:
        for message in resp['Messages']:
            messages.append(message["Body"])
    except Exception as e:
        print("Read Error: {}".format(str(e)))

    return messages

def get1Message(SQS, qURL):
    resp = SQS.receive_message(QueueUrl=qURL, AttributeNames=['All'], MaxNumberOfMessages=10, VisibilityTimeout=30)
    messages = []
    try:
        for message in resp['Messages']:
            messages.append(message["Body"])
    except Exception as e:
        print("Read Error: {}".format(str(e)))
    return messages

def main():
    try:
        ## TEST Removing random fields in the message
        # messages = get1Message(READ_SQS, READ_CONV_URL)
        # for message in messages:
        #     myDict = json.loads(message)
        #     for i in range(4):
        #         myDict.pop( random.choice( list(myDict.keys()) ) )   
        #     myDict["advertiser_id"] = "THISISATEST"
        #     resp = WRITE_SQS.send_message(QueueUrl=WRITE_CONV_URL, MessageBody=json.dumps(myDict))
        #     print(".",end="",flush=True)

        print("\nConversions\n")
        for i in range(0,5):
            messages = getMessages(READ_SQS, READ_CONV_URL)
            for message in messages:
                resp = WRITE_SQS.send_message(QueueUrl=WRITE_CONV_URL, MessageBody=message)
                print(".",end="",flush=True)

        print("\nTraffic\n")
        for i in range(0,5):
            messages = getMessages(READ_SQS, READ_TRAF_URL)
            for message in messages:
                resp = WRITE_SQS.send_message(QueueUrl=WRITE_TRAF_URL, MessageBody=message)
                print(".",end="",flush=True)

    except Exception as e:
        print("Some Error {}".format(str(e)))

if __name__ == '__main__':
    main()
