#!/bin/bash
docker run --privileged --name petal_bonds --net=host -v /server:/server -v /data:/data -dit petalbonds:v0.3 /usr/sbin/init
