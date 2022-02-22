import glob
from pathlib import Path
import re 
import json 

files = []

connections = []

for filename in glob.iglob("/home/kempy/Test/outputs/" + "**/**", recursive=True):
    path = Path(filename)
    if path.is_file():
        if filename not in files:
            files.append(filename)

for myfile in files:
    with open(myfile) as fp:
        dbinfo = {
            "EC2NAME": "",
            "PGS_URL": "",
            "DB_HOST": "",
            "DB_NAME": "",
            "DB_USER": "",
            "DB_PASS": ""
        }
        for line in fp:

            if line.startswith("DATABASE_"):
                line = line.strip()
                dbinfo["EC2NAME"] = myfile.split("/")[5]
                if any(ele in line for ele in ["DATABASE_URL=","DATABASE_READ_URL="]):
                    url = line.split("URL=")[1]
                    username = re.search("\/\/(.*?):", url)[1]
                    password = re.search(username + ":(.*?)@", url)[1]
                    host =  re.search(password.replace("$","\$") + "@(.*?)\/", url)[1]
                    database = re.search(host + "\/([a-z_]*)", url)[1]
                    dbinfo["PGS_URL"] = url
                    dbinfo["DB_HOST"] = host
                    dbinfo["DB_NAME"] = database
                    dbinfo["DB_USER"] = username
                    dbinfo["DB_PASS"] = password

                
            if line.startswith("DB_"):
                line = line.strip()
                dbinfo["EC2NAME"] = myfile.split("/")[5]
                if any(ele in line for ele in ["DB_HOST_PROD=","DB_HOST_MASTER=","DB_HOST="]):
                    dbinfo["DB_HOST"] = line.split("=")[1]
                if any(ele in line for ele in ["DB_NAME="]):
                    dbinfo["DB_NAME"] = line.split("=")[1]
                if any(ele in line for ele in ["DB_USERNAME=","DB_USERNAME_PROD="]):
                    dbinfo["DB_USER"] = line.split("=")[1]
                if any(ele in line for ele in ["DB_PASSWORD=","DB_PASSWORD_PROD="]):
                    dbinfo["DB_PASS"] = line.split("=")[1]
               
        if dbinfo["EC2NAME"] != "":
            connections.append(dbinfo)

print(json.dumps(connections,indent=2))

