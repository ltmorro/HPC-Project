#!/bin/sh
source `dirname "$0"`/common.sh

designate login
fix_shell

setup_nfs_client
setup_lustre_client

set_configured

wait_for_storage

reboot
