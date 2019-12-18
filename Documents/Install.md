# Installation Guides

* [Quick](#quick)
* [Manual](#manual)




## Quick

1. Start Mininet on Virtual Machine (VM) and login. For example:

	```sh
	$ ssh -Y mininet@vm
	$ ssh -Y mininet@192.168.56.3
	```

1. Clone this repository or download archived source code on your computer. 

	```sh 
	$ git clone git@csil-git1.cs.surrey.sfu.ca:471-project-6/sdn-routing.git 
	```

1. __From the same folder__, run the `sh install.sh` shell script to copy your local folder to the VM. If necessary, you can specify the IP address of the VM: `install.sh <IP>` (default = 192.168.56.3).

	```sh
	$ ./sdn-routing/install.sh 
	$ ./sdn-routing/install.sh 192.168.56.3
	```

1. While `install.sh` runs, it executes `ssh mininet@vm ~/sdn-routing/setup.sh` shell script to install the Python modules.
	
	```
	Installed /usr/local/lib/python2.7/dist-packages/TestNet-1.0-py2.7.egg
	Installed /usr/local/lib/python2.7/dist-packages/LSRouting-1.0-py2.7.egg
	```

1. When the script completes, you should this message:

	```
	All components were successfully installed
	Installed SDNetwork packages:
		TestNet: Create and test simulated SDNs
		Routing: Compute least-cost paths in a simulated SDN
	```

1. Now you can [run **TestNet**](#run-simulation) by executing one of:

	```sh
	$ sudo python ~/sdn-routing/run.py
	$ sudo ~/sdn-routing/run.py
	```

1. You can verify installation by listing the contents of home directory. Installed **sdn-routing** directory will appear there. 

	```sh
	$ ls ~
	install-mininet-vm.sh loxigen mininet oflops oftest openflow pox 'sdn-routing' ...
	```

1. To verify the modules were installed, print:

	```sh
	$ python -c 'from TestNet import *; print(dir());'
	['BabyTopo', 'CLI', 'LargeTopo', 'LinkTopo', 'Logger', 'RawWeightedLink', 'SmallTopo',   ...,   'wlinks']
	```


> _View **[sample output](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/1-install/install.sh.rtf)** of the installation script install.sh._  



&nbsp;
## Manual

1. If the installation script `install.sh` does not work for you, you can manually copy and install the project. First, use `scp -r` to copy the directory:

	```sh 
	$ scp -r /path/to/sdn-routing mininet@vm:~/sdn-routing
	```

1. On the VM, run the `setup.sh <parent-dir>` script to install Python packages:

	```sh
	$ ./sdn-network/setup.sh 'sdn-routing'
	```

1. Verify installation by listing the contents of Python distribution packages. Installed packages will appear there. 

	```sh 
	$ ls /usr/local/lib/python2.7/dist-packages/
	```

1. Now you can [run **TestNet**](#run-simulation) by executing one of:

	```sh
	$ sudo python ~/sdn-routing/run.py
	$ sudo ~/sdn-routing/run.py
	```


> _View **[sample output](https://csil-git1.cs.surrey.sfu.ca/471-project-6/sdn-routing/blob/master/docs/sample-outputs/1-install/setup.sh.rtf)** of the package setup script setup.sh._
