#!/bin/sh
source `dirname "$0"`/common.sh

designate login
fix_shell

set_configured

wait_for_storage

setup_nfs_client
setup_lustre_client

reboot
