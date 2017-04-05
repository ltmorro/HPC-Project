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
    node = request.XenVM('node' + str(i))
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS72-64-STD'
    iface = node.addInterface('if' + str(i))
    iface.addAddress(rspec.IPv4Address('192.168.1.' + str(i + 1), '255.255.255.0'))
    link.addInterface(iface)

    if i == 0:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo login >/root/designation'))

        node.cores = 1
        node.ram = 1024
        node.disk = 4

        node.routable_control_ip = True
    elif i == 1:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo storage >/root/designation'))

        node.cores = 1
        node.ram = 8192
        node.disk = 4

        bs = node.Blockstore('bs', '/mydata')
        bs.size = '1024GB'

        node.addService(rspec.Execute(shell='/bin/sh', command='yum install nfs-utils nfs-utils-lib'))
        node.addService(rspec.Execute(shell='/bin/sh', command='chkconfig nfs on; service rpcbind start; service nfs start'))
        node.addService(rspec.Execute(shell='/bin/sh', command='mkdir /storage'))
        node.addService(rspec.Execute(shell='/bin/sh', command='echo /storage *(rw,sync,no_root_squash,no_subtree_check) >/etc/exports'))
        node.addService(rspec.Execute(shell='/bin/sh', command='exportfs -a'))
    elif i == 2:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo gpu >/root/designation'))

        node.cores = 2
        node.ram = 8192
        node.disk = 4
    elif i == 3:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo large memory >/root/designation'))

        node.cores = 8
        node.ram = 65536
        node.disk = 4
    else:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo compute >/root/designation'))

        node.cores = 2
        node.ram = 8192
        node.disk = 4

portal.context.printRequestRSpec(request)
