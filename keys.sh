#!/bin/sh
cd /users

find * -mindepth 0 -maxdepth 0 -exec sudo -u {} mkdir -p /users/{}/.ssh \;
find * -mindepth 0 -maxdepth 0 -exec sudo -u {} ssh-keygen -P \'\' \;
find * -mindepth 0 -maxdepth 0 -exec sudo -u {} sh -c 'cat /users/{}/.ssh/id_rsa.pub | tee -a /users/{}/.ssh/authorized_keys' \;
