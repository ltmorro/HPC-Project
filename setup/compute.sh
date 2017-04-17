#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    wait_for_storage

    setup_nfs_client
    setup_lustre_client

    exit
fi

designate compute
fix_shell
fix_ssh

setup_mpi

install_lustre_client

set_configured

reboot
