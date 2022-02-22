#!/usr/bin/env python3

import sys
import boto3
import json
import inquirer
import subprocess

MAX_RESULTS = 20

class Colors(object):
    reset = "\033[0m"
    BIWhite ="\033[1;97m"
    White ="\033[0;37m"

def selectCluster(client):
    clusterNames = []
    xargs = { "maxResults": MAX_RESULTS }
    while xargs.get("nextToken") != "":
        response = client.list_clusters(**xargs)
        xargs["nextToken"] = response.get("nextToken","")
        for cluster in response.get("clusterArns",[]):
            try:
                clusterName = cluster.split("/")[1]
                if clusterName not in clusterNames:
                    clusterNames.append(clusterName)
            except:
                pass
    clusterNames.sort()
    clusters = [
        inquirer.List(
            "cluster",
            message="Select ECS Cluster?",
            choices=clusterNames,
        ),
    ]
    inq = inquirer.prompt(clusters)
    cluster = inq["cluster"]
    return cluster


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
    tasks = [
        inquirer.List(
            "task",
            message="Select ECS Task?",
            choices=taskArns,
        ),
    ]
    inq = inquirer.prompt(tasks)
    task = inq["task"]
    try:
        taskID = cluster.split("/")[2]
    except:
        taskID = task

    return taskID

def selectContainer(client, cluster, task):
    containerNames = []
    try:
        response = client.describe_tasks(cluster=cluster, tasks=[task])["tasks"][0]
        for container in response["containers"]:
            containerNames.append(container["name"])
    except:
        pass

    containerNames.sort()
    contain = [
        inquirer.List(
            "contain",
            message="Select ECS Container?",
            choices=containerNames,
        ),
    ]
    inq = inquirer.prompt(contain)
    contain = inq["contain"]
    return contain

def main(profile, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        client = session.client("ecs")
    except:
        print("Profile or Region ERROR. Please ensure you have logged into AWS.")
        exit(0)

    cluster = selectCluster(client)
    task = selectTask(client, cluster)
    container = selectContainer(client, cluster, task)

    subprocess.run(["aws", "ecs", "execute-command", "--cluster", cluster, "--task", task, "--container", container, "--profile", profile, "--region", region, "--command", "/bin/bash", "--interactive"])

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: {} {}<profile_name> <region>{}{}".format(sys.argv[0], Colors.BIWhite, Colors.White, Colors.reset))
        print("   eg: {} {}dev us-west-2{}{}".format(sys.argv[0], Colors.BIWhite, Colors.White, Colors.reset))
        exit(0)
    
    profile = sys.argv[1]
    region = sys.argv[2]

    main(profile, region)
