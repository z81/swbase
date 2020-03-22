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


for key in env.keys():
    if env[key] == "":
        print "Error %s is empty" % key
        exit(1)


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


webhookPath = "/usr/bin/webhook"

if os.path.isfile(webhookPath):
    print "Webhook exists"
else:
    print "Downloading webhook"
    webhookArchPath = os.path.join(BASE_PATH, "bin", "webhook") + ".tar.gz"
    webHookName = "webhook-" + osType + "-" + arch
    webHookExtractPath = os.path.join(webHookName, "webhook")

    url = "https://github.com/adnanh/webhook/releases/download/2.6.11/" + \
        webHookName + ".tar.gz"
    urllib.urlretrieve(url, webhookArchPath)

    print "Extracting webhook"
    run("tar -xvf " + webhookArchPath)

    # if os.rename(webHookExtractPath, webhookPath) == False:
    #     exit(2)

    # run("rm -r " + webHookName)
    # run("rm " + webhookArchPath)
    # run("chmod +x " + webhookPath)


print "Gitlab registry login"
os.system("docker login %s -u %s -p %s" %
          (env["GITLAB_SERVER"], env["GITLAB_LOGIN"], env["GITLAB_TOKEN"]))


print "Run docker-compose"
os.system("docker-compose -f %s/stacks/proxy/docker-compose.yaml up -d" % BASE_PATH)


template = """[Unit]
Description=Small server for creating HTTP endpoints (hooks)
Documentation=https://github.com/adnanh/webhook/

[Service]
ExecStart=webhook -nopanic -hotreload -hooks %s/hooks.json
WorkingDirectory=%s
User=root
Group=root

[Install]
WantedBy = multi - user.target """ % (BASE_PATH, BASE_PATH)

serviceFile = "/etc/systemd/system/webhook.service"


if osType == "linux" or osType == "freebsd":
    if os.path.isfile(serviceFile):
        print "systemd service exists"
    else:
        print "Create systemd service"
        f = open(serviceFile, "w+")
        f.write(template)
        f.close()

    os.system("service webhook start")
