#!/usr/bin/env python3

import boto3
import json
import random

QUEUE_CONVERSION = "FEAD-Sp-Conversion-Queue"
QUEUE_TRAFFIC = "FEAD-Sp-Traffic-Queue"

SESSION = boto3.Session(profile_name="prod")
SQS = SESSION.client("sqs", region_name="us-east-1")

def getQueueURL(QUEUE_NAME):
    q = SQS.get_queue_url(QueueName=QUEUE_NAME).get('QueueUrl')
    print("Queue URL is {}".format(str(q)))
    return q

def getMessages(qURL):
    resp = SQS.receive_message(QueueUrl=qURL, AttributeNames=['All'], MaxNumberOfMessages=10)
    try:
        for message in resp['Messages']:
            print(message["Body"],end="\n\n")
            print(type(message["Body"]),end="\n\n")
    except Exception as e:
        print("Read Error: {}".format(str(e)))

def main():
    try:
        uCon = getQueueURL(QUEUE_CONVERSION)
        uTra = getQueueURL(QUEUE_TRAFFIC)
        getMessages(uCon)
        getMessages(uTra)

    except Exception as e:
        print("Some Error {}".format(str(e)))

if __name__ == '__main__':
    main()
