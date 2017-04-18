#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    fix_ssh

    wait_for_storage

    setup_nfs_client
    setup_lustre_client

    exit
fi

designate large_memory
fix_shell

setup_mpi

install_lustre_client

set_configured

reboot
