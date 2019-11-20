# Link-State Routing in Software Defined Networking

Create a simulated software defined network and run least-cost paths Dijkstra's algorithm 


## Contents 

* [Description](#description)
* [Installation Guide](#installation-guide)
* [Preset Topologies](#preset-topologies)
* [Run Simulation](#run-simulation)
* [Authors](#authors)



## Description

_Project description..._

Project implements two modules:

1. **TestNet** - used to create and test software defined networks with switches implementing OpenFlow protocol. Networks are created using custom topology presets where each switch-to-switch link has a  weight assigned to it.
2. **LSRouting** -  performs link-state routing using Dikstra's least-cost paths algortihm. It is implemented in a standalone module separate from SDN controller. The output of the link-state algorithm is used to configure flow table entries. 



## Installation Guide

Clone this repository or download archived source code.

	git clone git@csil-git1.cs.surrey.sfu.ca:471-project-6/sdn-routing.git

Start Mininet virtual machine and login. For example,

	ssh -Y mininet@192.168.56.3

In the project's main directory _(renamed to SDNetwork)_, run the `instalnet.sh` script. It will copy all local files in SDNetwork folder to the VM's home directory and install both **TestNet** and **LSRouting** modules. You can specify the IP address of the VM: `installnet.sh <IP>` (default = 192.168.56.3).

	cd SDNetwork
	./installnet.sh 

	All components were successfully installed
	Installed SDNetwork packages:
		TestNet: Create and test simulated SDNs
		Routing: Compute least-cost paths in a simulated SDN
	
	Now you can create test networks by running:
		~/SDNetwork/run.py: create a test network (run as root).
		
You can verify installation by listing the contents of home directory. Installed SDNetwork directory will appear there. 

	ls ~
	install-mininet-vm.sh loxigen mininet oflops oftest openflow pox SDNetwork ...

## Preset Topologies

When you run You can choose from three different topology presets.  


## Run Simulation

Start **TestNet** using:

	sudo ~/SDNetwork/run.py

You will be prompted to choose one of the preset networks. 

	 < SELECT NETWORK > 
	 Choose one of the three network environments: 
		1. Tiny Network (default) - network with 4 switches and 5 links.
		2. Small Network - network with 6 switches and 10 links.
		3. Large Network - ...
	 (see network diagrams in the project definition) 
	 Input the index (1 to 3) of a network you want to test:  
	 ...
	 
