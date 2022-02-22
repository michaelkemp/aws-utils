import boto3
from datetime import datetime, timedelta
import time
import re

session = boto3.Session(profile_name="prod")
client = session.client('logs', region_name="us-east-1")

# query = 'fields @message | parse @message "[*]*" as loggingType, loggingMessage | filter loggingMessage like /marketplace_id/ | display loggingMessage'  
# query = 'fields @message | parse @message "[*]*" as loggingType, loggingMessage | filter loggingMessage like /SubscriptionConfirmation/ | display loggingMessage'  
query = 'fields @message' # | parse @message "[*]*" as loggingType, loggingMessage | display loggingMessage'  

log_groups = ['/aws/lambda/prod-fead-sp-to-snowflake-052702658761-conversion-lambda', '/aws/lambda/prod-fead-sp-to-snowflake-052702658761-traffic-lambda']

for log_group in log_groups:

    thisGroup = log_group.split("/")[-1]
    #outFile = open(thisGroup + ".txt", 'w')

    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=3)).timestamp()),
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

    count = 0    
    for result in response["results"]:
        for fields in result:
            if fields["field"] == "loggingMessage":
                message = re.findall("\{(.*?)\}", fields["value"])
                if len(message) == 1:
                    count += 1
                    print("{" + str(message[0]) + "}\n")
                    #outFile.write("{" + str(message[0]) + "}\n")
    print("\n{}\n".format(str(count)))
    #outFile.close()
