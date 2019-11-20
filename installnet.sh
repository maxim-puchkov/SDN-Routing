#!/bin/bash

#  install.sh
#  SDNetwork
#
#  Created by admin on 2019-11-20.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.


# Relative to install.sh directory
REL=$(dirname $0)

# Copy SDNetwork with TestNet and LinkStateRouting to VM
BUNDLE_DISPLAY_NAME="SDNetwork"
NET_LIB="TestNet"
LSR_LIB="Routing"
BUNDLE_DIR="${REL}/../${BUNDLE_DISPLAY_NAME}"

# ./installnet.sh <VM IP address>
# Default IP: 192.168.56.3
VM_IP="${1:-192.168.56.3}"
VM_BUNDLE_DIR="~/${BUNDLE_DISPLAY_NAME}"

# Names of executables scripts
SETUP="setup.sh"
RUN="run.py"

__done__() {
    tput setaf 2; tput bold; echo -e "\nAll components were successfully installed"; tput sgr0;
}
__error__() {
    tput setaf 1; tput bold; echo -e "\nUnable to install"; tput sgr0;
}
__cmd__() {
    tput setaf 5; tput bold; echo -n "${1}"; tput sgr0;
}


remove_bundle() {
    echo "Removing old SDNetwork files..."
    ( ssh mininet@${VM_IP} "if [ -d ${VM_BUNDLE_DIR} ]; then rm -r ${VM_BUNDLE_DIR}; fi; " \
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


show_info() {
    __done__
    echo -e "Installed ${BUNDLE_DISPLAY_NAME} packages:"
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
    echo ">> Running $(__cmd__ 'installnet') utility..."
    ( (remove_bundle && copy_bundle && set_privilege && install_packages && show_info) || (__error__) )
}

install
