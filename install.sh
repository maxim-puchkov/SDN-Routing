#!/bin/bash

#  install.sh
#  SDNetwork
#
#  Created by admin on 2019-11-20.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.


__done__() {
    tput setaf 2; tput bold; echo -e "\nAll components were successfully installed"; tput sgr0;
}
__error__() {
    tput setaf 1; tput bold; echo -e "\nUnable to install"; tput sgr0;
}
__cmd__() {
    tput setaf 5; tput bold; echo -n "${1}"; tput sgr0;
}


# Run the script from project parent folder
REL=$(dirname $0)
BUNDLE_ROOT=$(dirname $REL)
BUNDLE_NAME="${REL##*/}"
if [[ "${BUNDLE_NAME}" == "." ]]; then
	__error__
	echo "To install the files correcrly, run the script from the parent folder: "
	echo "	cd ../"
	echo "	./ProjectName/install.sh"
	echo
	exit 1
fi;
BUNDLE_DIR="${BUNDLE_ROOT}/${BUNDLE_NAME}"




# ./install.sh <VM IP address>
# Default IP: 192.168.56.3
VM_IP="${1:-192.168.56.3}"
VM_BUNDLE_DIR="~/${BUNDLE_NAME}"
VAR="${VM_BUNDLE_DIR}/var"


# Copy TestNet and LinkStateRouting to VM
NET_LIB="TestNet"
LSR_LIB="Routing"

# Names of executables scripts
SETUP="setup.sh"
RUN="run.py"


remove_bundle() {
    echo "Removing old ${BUNDLE_NAME} files..."
    ( ssh mininet@${VM_IP} "if [ -d ${VM_BUNDLE_DIR} ]; then sudo rm -r ${VM_BUNDLE_DIR}; fi;" \
    && echo "Deleted the '${VM_BUNDLE_DIR}' directory." )
}
copy_bundle() {
    echo "Copying files to remote host..."
    scp -r "${BUNDLE_DIR}" mininet@${VM_IP}:"${VM_BUNDLE_DIR}"
}
install_packages() {
    echo "Installing packages..."
    ssh mininet@${VM_IP} "chmod 0755 ${VM_BUNDLE_DIR}/${SETUP} && sh ${VM_BUNDLE_DIR}/${SETUP}"
}
set_privilege() {
    echo "Setting file access privilege..."
    ( ssh mininet@vm "chmod 0755 ${VM_BUNDLE_DIR}/${RUN}" \
    && echo -e "\t${RUN}: 0755" )
}


display_broadcast() {
    MSG="Installing..."
    echo -e "\t"$MSG | write $USER
}


show_info() {
    __done__
    echo -e "Installed ${BUNDLE_NAME} packages:"
    echo -e "\t$(__cmd__ ${NET_LIB}): Create and test simulated SDNs"
    echo -e "\t$(__cmd__ ${LSR_LIB}): Compute least-cost paths in a simulated SDN"

#    echo -e "\nTo use ${NET_LIB}, first run the setup script:"
#    echo -e "\t$(__cmd__ ${VM_BUNDLE_DIR}/${SETUP} build): setup package modules."

    echo -e "\nNow you can create test networks by running:"
    echo -e "\t$(__cmd__ ${VM_BUNDLE_DIR}/${RUN}): create a test network (run as root)."
#    echo -e "\t$(__cmd__ ${VM_BUNDLE_DIR}/...): ..."
    echo
}

install() {
    echo ">> Running $(__cmd__ 'install') utility..."
    ( (remove_bundle && copy_bundle && set_privilege && install_packages && show_info) || (__error__) )
}

install "${BUNDLE_NAME}"
