#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    exit
fi

designate gpu
fix_shell
fix_ssh

setup_mpi

set_configured

wait_for_storage

setup_nfs_client
setup_lustre_client

reboot
