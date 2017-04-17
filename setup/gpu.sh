#!/bin/sh
source `dirname "$0"`/common.sh

designate gpu
fix_shell

setup_nfs_client
setup_lustre_client

setup_mpi

set_configured

wait_for_storage

reboot
