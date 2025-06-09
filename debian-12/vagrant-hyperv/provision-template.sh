#!/bin/bash

# Provision generic box generic/debian12 with ansible and other useful aliases/utils

apt update
# upgrading postfix is always interactive, so must block it
apt-mark hold postfix 
apt upgrade -y
apt install -y ansible
echo "alias ll='ls -l'" >> /etc/profile
echo "alias python='python3'" >> /etc/profile