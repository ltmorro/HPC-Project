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
    iface.component_id = 'eth1'
    iface.addAddress(rspec.IPv4Address('192.168.1.' + str(i + 1), '255.255.255.0'))
    link.addInterface(iface)

    if i == 0:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo login >/root/designation'))
    elif i == 1:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo storage >/root/designation'))
        node.addService(rspec.Execute(shell='/bin/sh', command='yum install nfs-utils nfs-utils-lib'))
        node.addService(rspec.Execute(shell='/bin/sh', command='chkconfig nfs on; service rpcbind start; service nfs start'))
        node.addService(rspec.Execute(shell='/bin/sh', command='mkdir /storage'))
        node.addService(rspec.Execute(shell='/bin/sh', command='echo /storage *(rw,sync,no_root_squash,no_subtree_check) >/etc/exports'))
        node.addService(rspec.Execute(shell='/bin/sh', command='exportfs -a'))
    elif i == 2:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo gpu >/root/designation'))
    elif i == 3:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo large memory >/root/designation'))
    else:
        node.addService(rspec.Execute(shell='/bin/sh', command='sudo echo compute >/root/designation'))

portal.context.printRequestRSpec(request)
