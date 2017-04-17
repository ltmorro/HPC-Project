#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    wait_for_storage

    setup_nfs_client
    setup_lustre_client

    exit
fi

designate login
fix_shell
fix_ssh

install_lustre_client

set_configured

reboot
