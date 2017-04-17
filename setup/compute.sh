#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    exit
fi

designate compute
fix_shell

setup_mpi

set_configured

wait_for_storage

setup_nfs_client
setup_lustre_client

reboot
