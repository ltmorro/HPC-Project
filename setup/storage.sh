#!/bin/sh
source `dirname "$0"`/common.sh

if configured; then
    fix_ssh

    setup_lustre
    setup_scratch

    set_ready

    exit
fi

designate storage
fix_shell

setup_nfs

make_keys

install_lustre

set_configured

reboot
