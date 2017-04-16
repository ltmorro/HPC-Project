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
    node = request.XenVM('node' + str(i))
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS72-64-STD'
    iface = node.addInterface('if' + str(i))
    iface.addAddress(rspec.IPv4Address('192.168.1.' + str(i + 1), '255.255.255.0'))
    link.addInterface(iface)

    if i == 0:
        node.cores = 1
        node.ram = 1024

        node.routable_control_ip = True

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/login.sh'))
        node.addService(rspec.Execute(shell='sh', command='sudo /local/repository/login.sh'))
    elif i == 1:
        node.cores = 1
        node.ram = 8192

        bs1 = node.Blockstore('bs1', '/users')
        bs1.size = '64GB'
        bs2 = node.Blockstore('bs2', '/storage')
        bs2.size = '1024GB'

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/storage.sh'))
        node.addService(rspec.Execute(shell='sh', command='sudo /local/repository/storage.sh'))
    elif i == 2:
        node.cores = 2
        node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/gpu.sh'))
        node.addService(rspec.Execute(shell='sh', command='sudo /local/repository/gpu.sh'))
    elif i == 3:
        node.cores = 4
        node.ram = 16384

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/large_memory.sh'))
        node.addService(rspec.Execute(shell='sh', command='sudo /local/repository/large_memory.sh'))
    else:
        node.cores = 2
        node.ram = 8192

        node.addService(rspec.Execute(shell='sh', command='chmod +x /local/repository/compute.sh'))
        node.addService(rspec.Execute(shell='sh', command='sudo /local/repository/compute.sh'))

portal.context.printRequestRSpec(request)
