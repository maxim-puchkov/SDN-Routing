#!/bin/bash
# -*- coding: utf-8 -*-

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

# Names of executable scripts
SETUP="setup.sh"
RUN="run.py"
MAIN="__main__.py"



# Copy and install files
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
    ssh mininet@${VM_IP} "chmod 0755 ${VM_BUNDLE_DIR}/${SETUP} &&" \
        "sh ${VM_BUNDLE_DIR}/${SETUP} ${BUNDLE_NAME}"
}
set_privilege() {
    echo "Setting file access privilege..."
    ( ssh mininet@vm "chmod 0755 ${VM_BUNDLE_DIR}/${MAIN}" &&
        echo -e "\t${MAIN}: 0755" )
    ( ssh mininet@vm "chmod 0755 ${VM_BUNDLE_DIR}/${RUN}" &&
        echo -e "\t${RUN}: 0755" )
}



# Installation
install() {
    echo ">> Running $(__cmd__ 'install') utility..."
    ( (remove_bundle &&
        copy_bundle &&
        set_privilege &&
        install_packages &&
        show_info) ||
    (__error__) )
}
show_info() {
    __done__
    echo -e "Installed ${BUNDLE_NAME} packages:"
    echo -e "\t$(__cmd__ ${NET_LIB}): Create and test simulated SDNs"
    echo -e "\nNow you can create test networks by running:"
    echo -e "\t- $(__cmd__ 'sudo python '${BUNDLE_NAME})"
    echo -e "\t- $(__cmd__ 'sudo '${VM_BUNDLE_DIR}/${RUN})"
    echo
}



install "${BUNDLE_NAME}"
