#!/usr/bin/env python3

import boto3
import json
import random

QUEUE_CONVERSION = "Sp-Conversion"
QUEUE_TRAFFIC = "Sp-Traffic"

SESSION = boto3.Session(profile_name="dev")
SQS = SESSION.client("sqs", region_name="us-east-1")

names = ["Adam","Beth","Charles","Dayna","Eddie","Florence","Greg","Heidi"]
cars = ["Toyota","Dodge","Ford","Ferrari","Kia","Tesla","Nissan","Chevrolet"]
MESSAGE = {"name":"John", "age":30, "car":None}

def getQueueURL(QUEUE_NAME):
    q = SQS.get_queue_url(QueueName=QUEUE_NAME).get('QueueUrl')
    print("Queue URL is {}".format(str(q)))
    return q

def main():
    try:
        uCon = getQueueURL(QUEUE_CONVERSION)
        uTra = getQueueURL(QUEUE_TRAFFIC)
        for i in range(0,10):
            # MESSAGE["name"] = random.choice(names)
            # MESSAGE["car"] = random.choice(cars)
            # MESSAGE["age"] = random.randint(20,50)
            # data = json.dumps(MESSAGE)
            # #print(data)
            # resp = SQS.send_message(QueueUrl=uCon, MessageBody=data)
            # print(resp)

            MESSAGE["name"] = random.choice(names)
            MESSAGE["car"] = random.choice(cars)
            MESSAGE["age"] = random.randint(20,50)
            data = json.dumps(MESSAGE)
            print(type(data))
            resp = SQS.send_message(QueueUrl=uTra, MessageBody=data)
            print(resp)

    except Exception as e:
        print("Some Error {}".format(str(e)))

if __name__ == '__main__':
    main()
