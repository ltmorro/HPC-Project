#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    fix_ssh

    wait_for_storage

    setup_nfs_client
    setup_lustre_node

    exit
fi

designate compute
fix_shell

setup_module
setup_mpi

install_lustre

set_configured

reboot
