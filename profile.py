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

    if i == 0:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo login >/root/designation'))

        #node.cores = 1
        #node.ram = 1024

        node.routable_control_ip = True

        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo 192.168.1.2:/home /home nfs defaults 0 0 >>/etc/fstab'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo mount -a'))
    elif i == 1:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo storage >/root/designation'))

        #node.cores = 1
        #node.ram = 8192

        #bs1 = node.Blockstore('bs', '/home')
        #bs1.size = '64GB'
        #bs2 = node.Blockstore('bs', '/scratch')
        #bs2.size = '1024GB'

        bs1 = node.Blockstore('bs1', '/home')
        bs1.size = '1GB'
        bs2 = node.Blockstore('bs2', '/scratch')
        bs2.size = '1GB'

        node.addService(rspec.Execute(shell='/bin/sh', command='sudo yum install nfs-utils nfs-utils-lib'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo chkconfig nfs-server on; service rpcbind start; service nfs-server start'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo /home *(rw,sync,no_root_squash,no_subtree_check) >>/etc/exports'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo /scratch *(rw,sync,no_root_squash,no_subtree_check) >>/etc/exports'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo exportfs -a'))
    elif i == 2:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo gpu >/root/designation'))

        #node.cores = 2
        #node.ram = 8192

        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo 192.168.1.2:/home /home nfs defaults 0 0 >>/etc/fstab'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo mount -a'))
    elif i == 3:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo large memory >/root/designation'))

        #node.cores = 4
        #node.ram = 16384

        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo 192.168.1.2:/home /home nfs defaults 0 0 >>/etc/fstab'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo mount -a'))
    else:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo compute >/root/designation'))

        #node.cores = 2
        #node.ram = 8192
        node.ram = 1024

        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo 192.168.1.2:/home /home nfs defaults 0 0 >>/etc/fstab'))
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo mount -a'))

portal.context.printRequestRSpec(request)
