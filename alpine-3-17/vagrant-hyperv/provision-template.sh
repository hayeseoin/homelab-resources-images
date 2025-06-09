#!/bin/bash

apk update
apk upgrade
apk add git python3 ansible
echo "alias ll='ls -l'" >> /etc/profile
