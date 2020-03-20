#! /usr/bin/python
import os
import platform
import urllib

BASE_PATH = os.path.dirname(os.path.abspath(__file__ + '/../'))

env = dict()
with open(BASE_PATH + '/.env') as f:
    for line in f:
        key, value = line.split('=', 1)
        env[key] = value.replace('\n', '')

def run(cmd):
  os.system(cmd + " >> /dev/null")

dockerNetworkInspectCmd = "docker network inspect %s >> /dev/null" % env["NETWORK_NAME"]

if os.system(dockerNetworkInspectCmd) == 0:
  print "Network \"%s\" exist" % env["NETWORK_NAME"]
else:
  os.system("docker network create " + env["NETWORK_NAME"])
  print "Network \"%s\" created" % env["NETWORK_NAME"]


osType = platform.system().lower()
arch = platform.architecture()[0]
if arch == "64bit":
  arch = "amd64"
else:
  arch = "386"


print "Downloading webhook"
webhookPath = os.path.join(BASE_PATH, "bin", "webhook")
webhookArchPath = webhookPath + ".tar.gz"
webHookName = "webhook-" + osType + "-" + arch
webHookExtractPath = os.path.join(webHookName, "webhook")

url = "https://github.com/adnanh/webhook/releases/download/2.6.11/" + webHookName + ".tar.gz"
urllib.urlretrieve(url, webhookArchPath)
print "Extracting webhook"
run("tar -xvf " + webhookArchPath)
run("mv " + os.path.join(webHookName, "webhook") + " " + webhookPath)
run("rm -r " + webHookName)
run("rm " + webhookArchPath)
run("chmod +x " + webhookPath)
print "Run docker-compose"

os.system("docker-compose -f %s/stacks/proxy/docker-compose.yaml up -d" % BASE_PATH)
