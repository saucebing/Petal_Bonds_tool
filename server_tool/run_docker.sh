#!/bin/bash
docker run --privileged --name petal_bonds --net=host -v /server:/server -v /data:/data -dit centos:centos7.9.2009 /usr/sbin/init
