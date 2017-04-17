#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    setup_lustre
    set_ready

    exit
fi

designate storage
fix_shell

setup_nfs

make_keys

set_configured

install_lustre

reboot
