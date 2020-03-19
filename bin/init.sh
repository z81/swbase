#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
cd $BASEDIR

export $(egrep -v '^#' ../.env | xargs) >> /dev/null
echo $HOST_NAME

if (docker network inspect $NETWORK_NAME >/dev/null 2>&1) then
  echo "Network \"$NETWORK_NAME\" exist"
else
  echo "Create netork \"$NETWORK_NAME\":"
  docker network create $NETWORK_NAME
fi

docker-compose -f ../stacks/proxy/docker-compose.yaml up -d