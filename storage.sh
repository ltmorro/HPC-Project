#!/bin/sh
source `dirname "$0"`/common.sh

designate storage
fix_shell

setup_nfs
setup_lustre

make_keys

set_configured

reboot
