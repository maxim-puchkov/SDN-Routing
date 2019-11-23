# Link-State Routing in Software Defined Networking

Create a simulated software defined network and run least-cost paths Dijkstra's algorithm 



## Contents 

* [Description](#description)
* [Installation Guides](#installation-guides) 
    * [Quick](#quick)
    * [Manual](#manual)
* [Preset Networks](#preset-networks)
* [Run Simulation](#run-simulation)
* [Contributors](#contributors)



## Description

This project aims to simulate SDN LSRouting and data delivering using OpenFlow on small self-traffic network.

1. **TestNet** - used to create and test software defined networks with switches implementing OpenFlow protocol. Networks are created using custom topology presets where each switch-to-switch link has a  weight assigned to it.
2. **LSRouting** -  performs link-state routing using Dijkstra's least-cost paths algorithm. The results of the algorithm are used to configure flow table entries in every switch in the network. 



## Installation Guides

### Quick

Start Mininet Virtual Machine (VM) and login. For example:

	$ ssh -Y mininet@vm
	$ ssh -Y mininet@192.168.56.3

Clone this repository or download archived source code on your computer. 

	$ git clone git@csil-git1.cs.surrey.sfu.ca:471-project-6/sdn-routing.git

__From the same folder__, run the `install.sh` shell script to copy your local folder to the VM. If necessary, you can specify the IP address of the VM: `install.sh <IP>` (default = 192.168.56.3).

	$ ./sdn-routing/install.sh 
	$ ./sdn-routing/install.sh 192.168.56.3

While `install.sh` runs, it executes `ssh mininet@vm ~/sdn-routing/setup.sh ` shell script to install the Python modules.
	
	Installed /usr/local/lib/python2.7/dist-packages/TestNet-1.0-py2.7.egg
	Installed /usr/local/lib/python2.7/dist-packages/LSRouting-1.0-py2.7.egg
	
When the script completes, you should this message:
	
	All components were successfully installed
	Installed SDNetwork packages:
		TestNet: Create and test simulated SDNs
		Routing: Compute least-cost paths in a simulated SDN
	
Now you can [run **TestNet**](#run-simulation) by exectuing one of:

	$ sudo ~/sdn-routing/run.py
	$ sudo python ~/sdn-routing/run.py
		
You can verify installation by listing the contents of home directory. Installed **sdn-routing** directory will appear there. 

	$ ls ~
	install-mininet-vm.sh loxigen mininet oflops oftest openflow pox sdn-routing ...

To verify the modules were installed, print :

	$ python -c 'from TestNet import *; print(dir());'
	['BabyTopo', 'CLI', 'LargeTopo', 'LinkTopo', 'Logger', 'RawWeightedLink', 'SmallTopo', 		...,		 'wlinks']


### Manual

If the installation script `install.sh` does not work for you, you can use `scp -r` to copy the directory:

	$ scp -r /path/to/sdn-network mininet@vm:~/sdn-network
	
On the VM, run the `setup.sh <parent-dir>` script to install Python packages:

	$ ./sdn-network/setup.sh sdn-network

Verify installation by listing the contents of Python distribution packages. Installed packages will appear there. 

	$ ls /usr/local/lib/python2.7/dist-packages/

Now you can [run **TestNet**](#run-simulation) by exectuing one of:

	$ sudo ~/sdn-routing/run.py
	$ sudo python ~/sdn-routing/run.py



## Preset Networks

**TestNet** includes four preset networks. The name of a preset describes its relative size. Most presets were reconstructed from familiar examples to demonstrate the correctness of the routing algortihm.  

1. **Baby** – very small network with 3 switches and 3 links.
1. **Tiny** _(default)_ – simple network with 4 switches and 5 links in-between them.  
1. **Small** – a network with 6 switches and 10 links.
1. **Large** – ...

> If your input is invalid, the default network is selected.  



## Run Simulation

1. Run the **TestNet** simulation and choose a preset to create the chosen network.

		< SELECT NETWORK TOPOLOGY > 
		1. Baby Topo - very small network with 3 switches and 3 links.
		2. Tiny Topology (default) - simple network with 4 switches and 5 links in-between them.
		3. Small Topology - a network with 6 switches and 10 links.
		4. Large Topology - .
		(see network diagrams in the project definition) 
		Input the index (1 to 4) of a network you want to test:  

2. Next LSRouting algorithm will determine the shortest paths from hosts to hosts.


3. Upon selecting, the network will launch. The following tests will be conducted:

	1. **Initial Setup Test**: Check host reachability before adding flow tables.
		
		Expected results: The hosts should not reach other hosts because routing has not been set up yet. 

	1. **Routing Test**: Check host reachability after adding flow tables.
		
		Expected results: The hosts should reach other hosts after the controller constructs flow tables determined by the link-state routing algorithm. A path from one host to another has the lowest possible cost. 

	1. **Network Condtions Test**: Check host reachability after disabling a link. 
		
		Expected results: A link between two nodes is no longer available. Some hosts may lose connection to other hosts because their traffic is routed through that link. 
	
	1. **Second Routing Test**: Recompute the least-cost paths and update flow table entries considering the change in network conditions.
		
		Expected results: All hosts should be able to communicate. A path from one host to another has the lowest possible cost. 



## Contributors

Maxim Puchkov, Xiyu Zhang

>>>
November 21, 2019

Submission Commit: fc0d92894f57bba92ee192848637363dcf56e3d8
>>>
