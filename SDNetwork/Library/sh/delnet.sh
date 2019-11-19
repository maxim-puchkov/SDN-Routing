#!/bin/sh

#  delnet.sh
#  Completely remove the TestNet folder from VM
#
#  Created by admin on 2019-11-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

# Full remote path to TestNet directory (default)
REMOTE_DIR="~/TestNet"
BINARY_DIR="~/bin"


display_cmd() {
    tput setaf 5
    tput bold
    echo -n "${1}"
    tput sgr0
}

display_broadcast() {
    MSG="Deleting the ${REMOTE_DIR} folder."
#    ssh -o SendEnv=MSG mininet@vm "sudo wall -n '${MSG}'"
    echo -e "\t"$MSG | write $USER
}

delete_testnet() {
    ( ssh mininet@vm "rm -r ${REMOTE_DIR}" \
    && echo "Deleted the '${REMOTE_DIR}' directory." )
}

delete_binaries() {
    ( ssh mininet@vm "rm -r ${BINARY_DIR}" \
    && echo "Deleted the '${BINARY_DIR}' directory" )
}





# Delete TestNet from VM
__delnet__() {
    echo ">> Running $(display_cmd 'delnet') utility..."
    delete_testnet
#    delete_binaries
    echo "To reinstall TestNet, run the" \
         "$(display_cmd 'makenet') utility."
    echo
#    display_broadcast
}

# Usage:
#   'delnet'
__delnet__
