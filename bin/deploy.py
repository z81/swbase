#! /usr/bin/python
import os
import sys
import string

repName = sys.argv[1]

BASE_PATH = os.path.dirname(os.path.abspath(__file__ + '/../'))
STACKS_PATH = os.path.join(BASE_PATH, 'stacks')
REP_PATH = os.path.join(STACKS_PATH, repName)
REP_DOCKER_COMPOSE_PATH = os.path.join(REP_PATH, "docker-compose.yml")

if not os.path.isdir(REP_PATH):
    print REP_PATH + " is not exists"
    exit(1)

if not os.path.isfile(REP_DOCKER_COMPOSE_PATH):
    print REP_DOCKER_COMPOSE_PATH + " is not exists"
    exit(2)

cmd = string.join([
    "cd " + REP_PATH,
    "git pull",
    "docker-compose pull",
    "docker-compose down",
    "docker-compose up -d"
], " && ")

os.system(cmd)
