import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG

pc = portal.Context()
request = rspec.Request()

tourDescription = 'This profile sets up a mini cluster modeled after SDSC Comet.'

tourInstructions = """### Basic Instructions
Instantiate the profile and it should be ready to go with NFS users directory, Lustre scratch directory, OpenMPI, and mpi4py. For convenience, each user has an SSH key generated for them and OpenMPI is automatically added to users' profiles. These allows MPI programs to run out of the box without user configuration."""

tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
tour.Instructions(IG.Tour.MARKDOWN,tourInstructions)
request.addTour(tour)

link = request.LAN('lan')

for i in range(10):
    node = request.RawPC('node' + str(i))
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS72-64-STD'
    iface = node.addInterface('if' + str(i))
    iface.addAddress(rspec.IPv4Address('192.168.1.' + str(i + 1), '255.255.255.0'))
    link.addInterface(iface)

    node.addService(rspec.Execute(shell='sh', command="sudo -i su -c 'cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys'"))
    node.addService(rspec.Execute(shell='sh', command="sudo -i su -c 'cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys2'"))
    node.addService(rspec.Execute(shell='sh', command='''sudo -i su -c \\"sed -i -e 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config\\"'''))
    node.addService(rspec.Execute(shell='sh', command="sudo sed -i 's/\/bin\/tcsh/\/bin\/bash/g' /etc/passwd"))

    node.addService(rspec.Execute(shell='sh', command='echo \\"[e2fsprogs]\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"name=e2fsprogs\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"baseurl=https://downloads.hpdd.intel.com/public/e2fsprogs/latest/el7/\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"[lustre-client]\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"name=lustre-client\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7.3.1611/client/\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"[lustre-server]\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"name=lustre-server\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))
    node.addService(rspec.Execute(shell='sh', command='echo \\"baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7.3.1611/server/\\" | sudo tee -a /etc/yum.repos.d/lustre.repo'))

    node.addService(rspec.Execute(shell='sh', command='sudo yum -y --nogpgcheck install lustre-client'))

    if i == 0:
        node.addService(rspec.Execute(shell='sh', command='echo login | sudo tee /root/designation'))

        node.cores = 1
        node.ram = 1024

        node.routable_control_ip = True

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /oasis/scratch/comet'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        #node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0 | sudo tee -a /etc/fstab'))

    elif i == 1:
        node.addService(rspec.Execute(shell='sh', command='echo storage | sudo tee /root/designation'))

        node.cores = 1
        node.ram = 8192

        bs1 = node.Blockstore('bs1', '/users')
        bs1.size = '64GB'
        bs2 = node.Blockstore('bs2', '/storage')
        bs2.size = '1024GB'

        node.addService(rspec.Execute(shell='sh', command='sudo yum -y install nfs-utils nfs-utils-lib'))
        node.addService(rspec.Execute(shell='sh', command='sudo systemctl enable nfs-server'))
        node.addService(rspec.Execute(shell='sh', command='sudo systemctl start nfs-server'))
        node.addService(rspec.Execute(shell='sh', command='echo \\"/users *(rw,sync,no_root_squash,no_subtree_check)\\" | sudo tee -a /etc/exports'))
        node.addService(rspec.Execute(shell='sh', command='sudo exportfs -a'))

        node.addService(rspec.Execute(shell='sh', command='sudo yum -y --nogpgcheck install \\"*.el7_lustre\\" lustre'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /oasis/scratch/comet'))
        node.addService(rspec.Execute(shell='sh', command='sudo fallocate -l 1023410176000 /storage/scratch.img'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkfs.lustre --fsname=scratch --mgs --mdt --index=0 /storage/scratch.img'))
        #node.addService(rspec.Execute(shell='sh', command='echo /storage/scratch.img /oasis/scratch/comet lustre defaults 0 0 | sudo tee -a /etc/fstab'))

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/keys.sh'))
        node.addService(rspec.Execute(shell='sh', command='/local/repository/keys.sh'))

        node.addService(rspec.Execute(shell='sh', command='sudo touch /root/configured'))

        node.addService(rspec.Execute(shell='sh', command='sudo touch /root/reboot'))
    elif i == 2:
        node.addService(rspec.Execute(shell='sh', command='echo gpu | sudo tee /root/designation'))

        node.cores = 2
        node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /oasis/scratch/comet'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        #node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0 | sudo tee -a /etc/fstab'))
    elif i == 3:
        node.addService(rspec.Execute(shell='sh', command='echo large memory | sudo tee /root/designation'))

        node.cores = 4
        node.ram = 16384

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /oasis/scratch/comet'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        #node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2@tcp0:/scratch /oasis/scratch/comet lustre loop 0 0 | sudo tee -a /etc/fstab'))
    else:
        node.addService(rspec.Execute(shell='sh', command='echo compute | sudo tee /root/designation'))

        node.cores = 2
        node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir -p /oasis/scratch/comet'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        #node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2@tcp0:/scratch /oasis/scratch/comet lustre defaults 0 0 | sudo tee -a /etc/fstab'))

    #install openmpi on all nodes except the storage node
    if i != 1:
        node.addService(rspec.Execute(shell='sh', command='sudo yum install -y epel-release'))
        node.addService(rspec.Execute(shell='sh', command='sudo yum install -y python-devel python-pip'))
        node.addService(rspec.Execute(shell='sh', command='sudo yum install -y openmpi openmpi-devel'))
        node.addService(rspec.Execute(shell='sh', command='source /etc/profile'))
        node.addService(rspec.Execute(shell='sh', command="sudo -i su -c 'module load mpi/openmpi-x86_64; pip install mpi4py'"))
        node.addService(rspec.Execute(shell='sh', command='echo pml = ob1 | sudo tee -a /etc/openmpi-x86_64/openmpi-mca-params.conf'))
        node.addService(rspec.Execute(shell='sh', command='echo node2 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node2 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node3 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node3 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node3 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node3 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node4 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node4 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node5 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node5 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node6 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node6 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node7 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node7 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node8 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node8 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node9 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo node9 | sudo tee -a /etc/openmpi-x86_64/openmpi-default-hostfile'))
        node.addService(rspec.Execute(shell='sh', command='echo \\"module load mpi/openmpi-x86_64\\" | sudo tee -a /etc/bashrc'))

        # mark node as configured
        node.addService(rspec.Execute(shell='sh', command='sudo touch /root/configured'))

        # wait for storage node
        node.addService(rspec.Execute(shell='sh', command='until ssh node1 cat /root/configured; do sleep 10; done'))

        # reboot systems
        node.addService(rspec.Execute(shell='sh', command='sudo touch /root/reboot'))

portal.context.printRequestRSpec(request)
