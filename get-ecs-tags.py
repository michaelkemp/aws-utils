#!/usr/bin/env python3

import boto3, json

accounts = ["dev","prod","legacy"]

ecsClusters = {}

MAX_RESULTS = 20

def selectCluster(client):
    clusterArns = []
    xargs = { "maxResults": MAX_RESULTS }
    while xargs.get("nextToken") != "":
        response = client.list_clusters(**xargs)
        xargs["nextToken"] = response.get("nextToken","")
        for cluster in response.get("clusterArns",[]):
            if cluster not in clusterArns:
                    clusterArns.append(cluster)
    clusterArns.sort()
    return clusterArns


def selectTask(client, cluster):
    taskArns = []
    xargs = { "maxResults": MAX_RESULTS, "cluster": cluster, "desiredStatus": "RUNNING" }
    while xargs.get("nextToken") != "":
        response = client.list_tasks(**xargs)
        xargs["nextToken"] = response.get("nextToken","")
        for task in response.get("taskArns",[]):
            if task not in taskArns:
                taskArns.append(task)

    taskArns.sort()
    return taskArns



for account in accounts:
    print(account)
    for region in ["us-east-1", "us-west-2"]:
        print(region)
        session = boto3.Session(profile_name=account)
        client = session.client('ecs', region_name=region)
        clusters = selectCluster(client)
        for cluster in clusters:
            tasks = selectTask(client, cluster)
            ctags = []
            clusterTags = client.list_tags_for_resource( resourceArn=cluster )
            try:
                for tag in clusterTags["tags"]:
                    ctags.append({tag["key"]:tag["value"]})
            except:
                pass

            clusterTasks = {}
            for task in tasks:
                ttags = []
                taskTags = client.list_tags_for_resource( resourceArn=task )
                try:
                    for tag in clusterTags["tags"]:
                        ttags.append({tag["key"]:tag["value"]})
                except:
                    pass
                clusterTasks[task] = { "Tags": ttags }

            ecsClusters[cluster] = { "Account": account, "Region": region, "Tags": ctags, "Tasks": clusterTasks}

json_string = json.dumps(ecsClusters,indent=4)

with open('ecs-tags.json', 'w') as outfile:
	outfile.write(json_string)
