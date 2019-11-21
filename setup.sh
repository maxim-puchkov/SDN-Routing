#!/bin/bash

#  setup.sh
#  SDNetwork
#
#  Created by admin on 2019-11-20.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

# This script is run remotely to finish installation on the VM


# Relative to setup.sh directory
REL="$(dirname $0)"

# Copy SDNetwork with TestNet and LinkStateRouting to VM
BUNDLE_NAME="${1:-SDNetwork}"
NET_LIB="TestNet"
LSR_LIB="LSRouting"

# ./installnet.sh <VM IP address>
# Default IP: 192.168.56.3
VM_BUNDLE_DIR=~/${BUNDLE_NAME}

# Names of executables scripts
SETUP="setup.py"
RUN="run.py"

cleanup() {
	DIR="dist"
	EXT="egg-info"
	NET_BUILD="${NET_LIB}.${EXT}"
	sudo mv "${NET_BUILD}" "${DIR}/${NET_BUILD}"
	
	LSR_BUILD="${LSR_LIB}.${EXT}"
	sudo mv "${LSR_BUILD}" "${DIR}/${LSR_BUILD}"
	
	VAR="${VM_BUNDLE_DIR}/var"
	mkdir "${VAR}"
	sudo mv "${DIR}" "${VAR}/${DIR}"
	sudo rm -r "build"
}

# Install TestNet and LSRouting
install_packages() {
	VM_LIBRARY="${VM_BUNDLE_DIR}/${BUNDLE_NAME}/Library"
	
	TMP=~/${NET_LIB}
	mv "${VM_LIBRARY}/${NET_LIB}" "${TMP}"
	sudo python "${TMP}/${SETUP}" 'install'
	mv "${TMP}" "${VM_LIBRARY}/${NET_LIB}"
	
	TMP=~/${LSR_LIB}
	mv "${VM_LIBRARY}/${LSR_LIB}" "${TMP}"
	sudo python "${TMP}/${SETUP}" 'install'
	mv "${TMP}" "${VM_LIBRARY}/${LSR_LIB}"

}


install_packages
cleanup
