# Link-State Routing in Software Defined Networking

Create a simulated software defined network and run least-cost paths Dijkstra's algorithm


## Contents 

* [Description](#description)
* [Installation Guides](#installation-guides) 
    * [Quick](#quick)
    * [Manual](#manual)
* [Preset Networks](#preset-networks)
* [Run Simulation](#run-simulation)
	* [Commands](#debugging-commands)
	* [Capture Network Traffic](#wireshark)
* [Contributors](#contributors)





&nbsp;
# Description

This project aims to simulate SDN LSRouting and data delivering using OpenFlow on small self-traffic network.

1. **TestNet** - used to create and test software defined networks with switches implementing OpenFlow protocol. Networks are created using custom topology presets where each switch-to-switch link has a  weight assigned to it.
2. **LSRouting** -  performs link-state routing using Dijkstra's least-cost paths algorithm. The results of the algorithm are used to configure flow table entries in every switch in the network. 





&nbsp;
# Installation Guides

### Quick

1. Start Mininet on Virtual Machine (VM) and login. For example:

		$ ssh -Y mininet@vm
		$ ssh -Y mininet@192.168.56.3

1. Clone this repository or download archived source code on your computer. 

		$ git clone git@csil-git1.cs.surrey.sfu.ca:471-project-6/sdn-routing.git

1. __From the same folder__, run the `install.sh` shell script to copy your local folder to the VM. If necessary, you can specify the IP address of the VM: `install.sh <IP>` (default = 192.168.56.3).

		$ ./sdn-routing/install.sh 
		$ ./sdn-routing/install.sh 192.168.56.3

1. While `install.sh` runs, it executes `ssh mininet@vm ~/sdn-routing/setup.sh ` shell script to install the Python modules.
	
		Installed /usr/local/lib/python2.7/dist-packages/TestNet-1.0-py2.7.egg
		Installed /usr/local/lib/python2.7/dist-packages/LSRouting-1.0-py2.7.egg
	
1. When the script completes, you should this message:
	
		All components were successfully installed
		Installed SDNetwork packages:
			TestNet: Create and test simulated SDNs
			Routing: Compute least-cost paths in a simulated SDN
	
1. Now you can [run **TestNet**](#run-simulation) by exectuing one of:

		$ sudo ~/sdn-routing/run.py
		$ sudo python ~/sdn-routing/run.py
		
1. You can verify installation by listing the contents of home directory. Installed **sdn-routing** directory will appear there. 

		$ ls ~
		install-mininet-vm.sh loxigen mininet oflops oftest openflow pox sdn-routing ...

1. To verify the modules were installed, print:

		$ python -c 'from TestNet import *; print(dir());'
		['BabyTopo', 'CLI', 'LargeTopo', 'LinkTopo', 'Logger', 'RawWeightedLink', 'SmallTopo', 		...,		 'wlinks']

> _View **[sample output](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/1-install/install.sh.rtf)** of the installation script **install.sh**_  



&nbsp;
## Manual

1. If the installation script `install.sh` does not work for you, you can manually copy and install the project. First, use `scp -r` to copy the directory:

		$ scp -r /path/to/sdn-network mininet@vm:~/sdn-network
	
1. On the VM, run the `setup.sh <parent-dir>` script to install Python packages:

		$ ./sdn-network/setup.sh sdn-network

1. Verify installation by listing the contents of Python distribution packages. Installed packages will appear there. 

		$ ls /usr/local/lib/python2.7/dist-packages/

1. Now you can [run **TestNet**](#run-simulation) by exectuing one of:

		$ sudo ~/sdn-routing/run.py
		$ sudo python ~/sdn-routing/run.py

> _View **[sample output](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/1-install/setup.sh.rtf)** of the package setup script **setup.sh**_


&nbsp;
# Preset Networks

**TestNet** includes four preset networks. The name of a preset describes its relative size. Most presets were reconstructed from familiar examples to demonstrate the correctness of the routing algortihm. If your input is invalid, the default network is selected.

1. **Baby** – very small network with 3 switches and 3 links _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/diagrams/1-Baby-Diagram.png)_.
1. **Tiny** _(default)_ – simple network with 4 switches and 5 links in-between them _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/diagrams/2-Tiny-Diagram.png)_.
1. **Small** – a network with 6 switches and 10 links _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/diagrams/3-Small-Diagram.png)_.
1. **Large** – _(debug)_ _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/diagrams/4-Large-Diagram.png)_.

> _View all network diagrams **[here](#https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/tree/master/docs/diagrams)**_ 





&nbsp;
# Run Simulation

### Select Network 

1. Run the **TestNet** simulation and choose a preset to create the chosen network.

		< SELECT NETWORK TOPOLOGY > 
		1. Baby Topo - very small network with 3 switches and 3 links.
		2. Tiny Topology (default) - simple network with 4 switches and 5 links in-between them.
		3. Small Topology - a network with 6 switches and 10 links.
		4. Large Topology - .
		(see network diagrams in the project definition) 
		Input the index (1 to 4) of a network you want to test:  

1. Configuration command-line interface (CLI) will start. Here you can enter commands to monitor network traffic (`tcpdump`, `wireshark`, etc.) or view initial network configuration (`all`, `flows`). Type `exit` to exit the configuration phase and begin the tests.

1. Next **LSRouting** algorithm will determine the shortest paths from hosts to hosts.

1. Upon selecting, the network will launch. The following tests will be conducted:


	1. **Initial Setup Test**: Check host reachability before adding flow tables.
		
		Expected results: The hosts should not reach other hosts because routing has not been set up yet. 

	1. **Routing Test**: Check host reachability after adding flow tables.
		
		Expected results: The hosts should reach other hosts after the controller constructs flow tables determined by the link-state routing algorithm. A path from one host to another has the lowest possible cost. 

	1. **Network Condtions Test**: Check host reachability after disabling a link. 
		
		Expected results: A link between two nodes is no longer available. Some hosts may lose connection to other hosts because their traffic is routed through that link. 
	
	1. **Second Routing Test**: Recompute the least-cost paths and update flow table entries considering the change in network conditions.
		
		Expected results: All hosts should be able to communicate. A path from one host to another has the lowest possible cost. 


1. When the tests finish, you another CLI will start. View network statistics with `all` or any other debugging command. Type `exit` to exit the simulation phase and leave.

> _View [sample outputs](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/tree/master/docs/sample-outputs/3-Network-Simulation)_ 


&nbsp;
## Debugging Commands

* Multiple commands _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/2-CLI-commands/all-sample.rtf)_:
	* `all` – run multiple relevant tests on a network, one by one
* Link-State routing _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/2-CLI-commands/routes-sample.rtf)_:
	* `weights` – weight of links
	* `costs` – cost of the lowest-cost path to samevery switch
	* `routes` – first-hop switches with the lowest cost
	* `paths` – all shortest paths
* OpenFlow _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/2-CLI-commands/flows-sample.rtf)_:
	* `stats` – traffic statistics for each switch
	* `flows` – flow table entries of every switch
	*  `deleteFlows` – delete all flows
* Run on every node _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/2-CLI-commands/other-sample.rtf)_:
	* `ips` – IP addresses
	* `arps` – ARP caches
	* `netstats` – routing tables
	* `ifconfigs` – interface configurations


&nbsp;
## Wireshark

* Tiny Network:
	1. Initially, **Host 1** cannot reach **Host 2** because the flow tables of SDN-conrolled switches are not computed. **Wireshark** and **tcpdump** show that **Host 1** sends 3 ARP packets to find **Host 2**, but does not receive a reply _[(image)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/4-wireshark-tcpdump/1-ping-s1-s2-fail.png)_.
	1. When the flows tables are computed and updated, the least-cost path from **Switch 1** to **Switch 2** is going through **Switch 4**. The packets from **Host 1** travel to **Switch 1** (left), **Switch 4** (middle), and then **Switch 2** (right) before reaching the destination **Host 2** _[(image)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/4-wireshark-tcpdump/2-ping-s1-s2-via-s4.png)_.
	1. **Host 2** replies to **Host 1**. 





&nbsp;
# Contributors

* **Maxim Puchkov** 
* **Xiyu Zhang**



>>>
Date: November 21, 2019

GitLab repository: https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing.git

Submission commit: fc0d92894f57bba92ee192848637363dcf56e3d8
>>>
