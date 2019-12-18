# Link-State Routing in Software Defined Networking

Create a simulated software defined network and run least-cost paths Dijkstra's algorithm.


### Contents

* [Description](#description)
* [Installation Guides](#installation-guides) 
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

Clone the repository, install Python packages on the VM, and run `run.py` script. 


 > _View detailed **[installation instructions](Documents/Install.md)**._
 
 <!-- URL:
https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/Install.md -->





&nbsp;
# Preset Networks

**TestNet** includes multiple preset networks. The name of a preset describes its relative size. Most presets were reconstructed from familiar examples to demonstrate correctness of the routing algorithm.

1. **Baby** – very small network with 3 switches and 3 links _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/Diagrams/1-Baby-Diagram.png)_.
1. **Tiny** _(default)_ – simple network with 4 switches and 5 links in-between them _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/Diagrams/2-Tiny-Diagram.png)_.
1. **Small** – a network with 6 switches and 10 links _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/Diagrams/3-Small-Diagram.png)_.
1. ... <!-- **Large** – _(debug)_ _[(network diagram)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/Diagrams/4-Large-Diagram.png)_. -->
1. ... <!-- **Massive** – 200 switches and 1,000 links. -->


> _View all network diagrams [here](#https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/tree/master/Documents/Diagrams)._ 





&nbsp;
# Run Simulation

### Select Network 

1. Run a **TestNet** simulation.

	```sh
	$ sudo python ~/sdn-routing/run.py
	```

1. Choose a preset network from the list.

	```		
	< SELECT NETWORK TOPOLOGY > 
	1. Baby Topology - very small network with 3 switches and 3 links.
	2. Tiny Topology (default) - simple network with 4 switches and 5 links.
	3. Small Topology - a network with 6 switches and 10 links.
	4. Large Topology - network of 16 connected switches (debug).
	5. Massive Topology - 200 switches and 1000 links, on average (debug).
	(see network diagrams in the project definition) 
	Input the index (1 to 5) of a network you want to test:
	```

1. First configuration command-line interface (CLI) will start. Here you can enter commands to monitor network traffic (`tcpdump`, `wireshark`, etc.) or view initial network configuration (`all`, `flows`, [etc.](#debugging-commands)). 

	```
	< STARTING CONFIGURATION INTERFACE > 
	Input commands (optional):
	(E.g., track packets with 'sudo wireshark &', 'tcpdump', etc.)
	When you are ready to start the simulation tests, type 'exit' or press CTRL-D.
	```

1. Type `exit` to exit the configuration phase and begin the tests. Upon selecting, the network will launch. Next **LSRouting** algorithm will determine the shortest paths from hosts to hosts. The following tests will be conducted:

	```
	TestNet> exit

	< RUNNING TESTS... >
	```


	1. **Initial Setup Test**: Check host reachability before adding flow tables.
		
		Expected results: The hosts should not reach other hosts because routing has not been set up yet. 

	1. **Routing Test**: Check host reachability after adding flow tables.
		
		Expected results: The hosts should reach other hosts after the controller constructs flow tables determined by the link-state routing algorithm. A path from one host to another has the lowest possible cost. 

	1. **Network Conditions Test**: Check host reachability after disabling a link. 
		
		Expected results: A link between two nodes is no longer available. Some hosts may lose connection to other hosts because their traffic is routed through that link. 
	
	1. **Second Routing Test**: Recompute the least-cost paths and update flow table entries considering the change in network conditions.
		
		Expected results: All hosts should be able to communicate. A path from one host to another has the lowest possible cost. 


1. When the tests finish, the second CLI will start. View network statistics with `all` or any other debugging command. Type `exit` to exit the simulation phase and leave.


> _View [sample outputs](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/tree/master/Documents/SampleOutputs/3-Simulation)._



&nbsp;
## Debugging Commands

* Multiple commands _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/2-CLI-Commands/all-sample.rtf)_:
	* `all` – run multiple relevant tests on a network, one by one
* Link-State routing _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/2-CLI-Commands/routes-sample.rtf)_:
	* `weights` – weight of links
	* `costs` – cost of the lowest-cost path to every other switch
	* `routes` – first-hop switches with the lowest cost
	* `paths` – all shortest paths
* OpenFlow _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/2-CLI-Commands/flows-sample.rtf)_:
	* `stats` – traffic statistics for each switch
	* `flows` – flow table entries of every switch
	*  `deleteFlows` – delete all flows
* Run on every node _[(sample output)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/2-CLI-Commands/other-sample.rtf)_:
	* `ips` – IP addresses
	* `arps` – ARP caches
	* `netstats` – routing tables
	* `ifconfigs` – interface configurations



&nbsp;
## Wireshark

* Tiny Network:
	1. Initially, **Host 1** cannot reach **Host 2** because the flow tables of SDN-controlled switches are not computed. **Wireshark** and **tcpdump** show that **Host 1** sends 3 ARP packets to find **Host 2**, but does not receive a reply _[(image)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/4-Wireshark/1-ping-s1-s2-fail.png)_.
	1. When the flows tables are computed and updated, the least-cost path from **Switch 1** to **Switch 2** is going through **Switch 4**. The packets from **Host 1** travel to **Switch 1** (left), **Switch 4** (middle), and then **Switch 2** (right) before reaching the destination **Host 2** _[(image)](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/Documents/SampleOutputs/4-Wireshark/2-ping-s1-s2-via-s4.png)_.
	1. **Host 2** replies to **Host 1**. 





&nbsp;
# Contributors

* Maxim Puchkov
* Xiyu Zhang

_See latest [CHANGES.md](CHANGES.md) (display as [plaintext](CHANGES.txt))._


&nbsp;
>>>
GitLab repository: https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing.git

Submission commit: fc0d92894f57bba92ee192848637363dcf56e3d8 (Nov 21, 2019)

Presentation commit: 8608fcc5712eef882d29a005759e99982857abb0 (Nov 26, 2019)
>>>
