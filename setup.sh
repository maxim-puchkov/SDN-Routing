#!/bin/bash

#  setup.sh
#  SDNetwork
#
#  Created by admin on 2019-11-20.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

# Relative to install.sh directory
REL=$(dirname $0)

# Copy SDNetwork with TestNet and LinkStateRouting to VM
BUNDLE_DISPLAY_NAME="SDNetwork"
NET_LIB="TestNet"
LSR_LIB="LSRouting"
BUNDLE_DIR=$REL/../$BUNDLE_DISPLAY_NAME

# ./installnet.sh <VM IP address>
# Default IP: 192.168.56.3
VM_IP="$1:-192.168.56.3"
VM_BUNDLE_DIR=~/$BUNDLE_DISPLAY_NAME

# Names of executables scripts
SETUP="setup.py"
RUN="run.py"


# Install TestNet and LSRouting
install_packages() {
	VM_LIBRARY=$VM_BUNDLE_DIR/SDNetwork/Library
	
	TMP=~/$NET_LIB
	mv $VM_LIBRARY/$NET_LIB $TMP
	sudo python $TMP/$SETUP install
	mv $TMP $VM_LIBRARY/$NET_LIB
	
	TMP=~/$LSR_LIB
	mv $VM_LIBRARY/$LSR_LIB $TMP
	sudo python $TMP/$SETUP install
	mv $TMP $VM_LIBRARY/$LSR_LIB

}


install_packages
