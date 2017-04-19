#!/bin/bash
storage=192.168.1.2

designate() {
    echo "$1" >/root/designation
}

set_configured() {
    touch /root/configured
}

set_ready() {
    touch /root/ready
}

alias configured='test -e /root/configured'

fix_shell() {
    sed -i -e 's#/bin/tcsh#/bin/bash#g' /etc/passwd
}

fix_ssh() {
    echo -e "\tStrictHostKeyChecking no" >>/etc/ssh/ssh_config
    cat /root/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys
    cat /root/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys2
}

make_keys() {
    pushd /users
    find * -mindepth 0 -maxdepth 0 -not -path lost+found -exec sudo -u {} mkdir -p /users/{}/.ssh \;
    yes '' | find * -mindepth 0 -maxdepth 0 -not -path lost+found -exec sudo -u {} ssh-keygen -P '' \;
    find * -mindepth 0 -maxdepth 0 -not -path lost+found -exec sudo -u {} sh -c 'cat /users/{}/.ssh/id_rsa.pub >>/users/{}/.ssh/authorized_keys' \;
    popd
}

setup_nfs() {
    yum -y install nfs-utils nfs-utils-lib
    systemctl enable nfs-server
    systemctl start nfs-server
    echo "/users *(rw,sync,no_root_squash,no_subtree_check)" >>/etc/exports
    exportfs -a
}

setup_nfs_client() {
    rm -rf /users
    mkdir -p /users
    echo "192.168.1.2:/users /users nfs defaults 0 0" >>/etc/fstab
    mount /users
}

setup_lustre_repo() {
    echo "[e2fsprogs]" >>/etc/yum.repos.d/lustre.repo
    echo "name=e2fsprogs" >>/etc/yum.repos.d/lustre.repo
    echo "baseurl=https://downloads.hpdd.intel.com/public/e2fsprogs/latest/el7/" >>/etc/yum.repos.d/lustre.repo
    echo "[lustre-client]" >>/etc/yum.repos.d/lustre.repo
    echo "name=lustre-client" >>/etc/yum.repos.d/lustre.repo
    echo "baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7.3.1611/client/" >>/etc/yum.repos.d/lustre.repo
    echo "[lustre-server]" >>/etc/yum.repos.d/lustre.repo
    echo "name=lustre-server" >>/etc/yum.repos.d/lustre.repo
    echo "baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7.3.1611/server/" >>/etc/yum.repos.d/lustre.repo
}

install_lustre() {
    setup_lustre_repo

    yum -y --nogpgcheck install "kernel-*.el7_lustre" lustre

    echo "options lnet networks=tcp0(eth1)" >>/etc/modprobe.d/lustre.conf
}

setup_lustre() {
    mkdir -p /mnt/mdt
    mkdir -p /mnt/ost0

    fallocate -l 1G /storage/mdt.img
    mkfs.lustre --fsname=scratch --mgs --mdt --index=0 /storage/mdt.img
    echo "/storage/mdt.img /mnt/mdt lustre loop 0 0" >>/etc/fstab
    mount /mnt/mdt

    fallocate -l 939G /storage/ost0.img
    mkfs.lustre --fsname=scratch --mgsnode="$storage@tcp0" --ost --index=0 /storage/ost0.img
    echo "/storage/ost0.img /mnt/ost0 lustre loop 0 0" >>/etc/fstab
    mount /mnt/ost0

    mkdir -p /oasis/scratch/comet
    echo "$storage@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0" >>/etc/fstab
    mount /oasis/scratch/comet
}

setup_scratch() {
    pushd /users
    find * -mindepth 0 -maxdepth 0 -not -path lost+found -exec sudo mkdir -p /oasis/scratch/comet/{} \;
    find * -mindepth 0 -maxdepth 0 -not -path lost+found -exec sudo chown {}:pdc-edu-lab-PG0 /oasis/scratch/comet/{} \;
    popd
}

setup_lustre_node() {
    number="$(hostname | cut -d. -f1 | sed -e 's/node//' | xargs -I. expr . - 1)"

    mkdir -p /mnt/ost"$number"
    fallocate -l 939G /storage/ost"$number".img
    mkfs.lustre --fsname=scratch --mgsnode="$storage@tcp0" --ost --index="$number" /storage/ost"$number".img
    echo "/storage/ost"$number".img /mnt/ost$number lustre loop 0 0" >>/etc/fstab
    mount /mnt/ost"$number"

    mkdir -p /oasis/scratch/comet
    echo "$storage@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0" >>/etc/fstab
    mount /oasis/scratch/comet
}

setup_lustre_client() {
    mkdir -p /oasis/scratch/comet
    echo "$storage@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0" >>/etc/fstab
    mount /oasis/scratch/comet
}

setup_module() {
    yum install -y environment-modules
}

setup_mpi() {
    yum install -y epel-release
    yum install -y python-devel python-pip
    yum install -y openmpi openmpi-devel

    source /etc/profile
    module load mpi/openmpi-x86_64
    pip install mpi4py

    echo "pml = ob1" >>/etc/openmpi-x86_64/openmpi-mca-params.conf
    echo node2 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node2 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node3 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node3 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node3 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node3 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node4 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node4 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node5 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node5 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node6 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node6 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node7 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node7 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node8 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node8 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node9 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo node9 >>/etc/openmpi-x86_64/openmpi-default-hostfile
    echo "module load mpi/openmpi-x86_64" >>/etc/bashrc
}

wait_for_storage() {
    until ssh node1 cat /root/ready; do
        sleep 10
    done
}
