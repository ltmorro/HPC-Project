import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG

pc = portal.Context()
request = rspec.Request()

tourDescription = 'This profile sets up a mini cluster modeled after SDSC Comet.'

tourInstructions = \
"""
### Basic Instructions
None yet.
"""

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

    if i == 0:
        node.addService(rspec.Execute(shell='sh', command='echo login | sudo tee /root/designation'))

        #node.cores = 1
        #node.ram = 1024

        node.routable_control_ip = True

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /scratch'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/scratch /scratch nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='sudo mount -a'))
        node.addService(rspec.Execute(shell='sh', command='''sudo -i su -c \\"sed -i -e 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config\\"'''))

    elif i == 1:
        node.addService(rspec.Execute(shell='sh', command='echo storage | sudo tee /root/designation'))

        #node.cores = 1
        #node.ram = 8192

        #bs1 = node.Blockstore('bs', '/users')
        #bs1.size = '64GB'
        #bs2 = node.Blockstore('bs', '/scratch')
        #bs2.size = '1024GB'

        bs1 = node.Blockstore('bs1', '/users')
        bs1.size = '1GB'
        bs2 = node.Blockstore('bs2', '/scratch')
        bs2.size = '1GB'

        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /scratch'))
        node.addService(rspec.Execute(shell='sh', command='sudo yum install nfs-utils nfs-utils-lib'))
        node.addService(rspec.Execute(shell='sh', command='sudo systemctl enable nfs-server'))
        node.addService(rspec.Execute(shell='sh', command='sudo systemctl start nfs-server'))
        node.addService(rspec.Execute(shell='sh', command='echo \\"/users *(rw,sync,no_root_squash,no_subtree_check)\\" | sudo tee -a /etc/exports'))
        node.addService(rspec.Execute(shell='sh', command='echo \\"/scratch *(rw,sync,no_root_squash,no_subtree_check)\\" | sudo tee -a /etc/exports'))
        node.addService(rspec.Execute(shell='sh', command='sudo exportfs -a'))
    elif i == 2:
        node.addService(rspec.Execute(shell='sh', command='echo gpu | sudo tee /root/designation'))

        #node.cores = 2
        #node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /scratch'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/scratch /scratch nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='sudo mount -a'))
    elif i == 3:
        node.addService(rspec.Execute(shell='sh', command='echo large memory | sudo tee /root/designation'))

        #node.cores = 4
        #node.ram = 16384

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /scratch'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/scratch /scratch nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='sudo mount -a'))
    else:
        node.addService(rspec.Execute(shell='sh', command='echo compute | sudo tee /root/designation'))

        #node.cores = 2
        #node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='sudo rm -rf /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /users'))
        node.addService(rspec.Execute(shell='sh', command='sudo mkdir /scratch'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/users /users nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='echo 192.168.1.2:/scratch /scratch nfs defaults 0 0 | sudo tee -a /etc/fstab'))
        node.addService(rspec.Execute(shell='sh', command='sudo mount -a'))

    #install openmpi on all nodes except the storage node
    if i != 1:
	    node.addService(rspec.Execute(shell='sh', command='sudo yum install -y epel-release'))
	    node.addService(rspec.Execute(shell='sh', command='sudo yum install -y python-devel python-pip'))
	    node.addService(rspec.Execute(shell='sh', command='sudo yum install -y openmpi openmpi-devel'))
	    node.addService(rspec.Execute(shell='sh', command='source /etc/profile'))
	    node.addService(rspec.Execute(shell='sh', command="sudo -i su -c 'module load mpi/openmpi-x86_64; pip install mpi4py'"))
            node.addService(rspec.Execute(shell='sh', command='echo \\"module load mpi/openmpi-x86_64\\" | sudo tee -a /etc/bashrc'))
            node.addService(rspec.Execute(shell='sh', command='''echo \\"alias mpirun='mpirun --allow-run-as-root -mca btl ^openib -host node0,node2,node3,node4,node5,node6,node7,node8,node9 '\\" | sudo tee -a /etc/bashrc'''))

portal.context.printRequestRSpec(request)
