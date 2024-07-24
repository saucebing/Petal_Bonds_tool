#!/bin/bash
docker run --privileged --name petal_bonds --net=host -v /server:/server -v /data:/data -dit docker.io/saucebing/petalbonds:v0.5 /usr/sbin/init
