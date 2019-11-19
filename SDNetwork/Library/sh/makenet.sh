#!/bin/sh

#  makenet.sh
#  Upload TestNet source files to VM
#
#  Created by admin on 2019-11-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

# Name of the main and help library scripts
LIB="TestNet"
BIN="bin"
#MAIN_SCRIPT="${LIB}Bundle.py"
MAIN_SCRIPT="main.py"
HELP_SCRIPT="help.py"
BUNDLE="/Users/admin/Developer/Projects/macOS/SDNetwork/SDNetwork/"

# Full local path to TestNet directory (default)
DEF_LOCAL_DIR="${BUNDLE}/Library/${LIB}"
# Full remote path to TestNet directory (default)
DEF_REMOTE_DIR="~/${LIB}"




display_cmd() {
	tput setaf 5
	tput bold
	echo -n "${1}"
	tput sgr0
}

# Read custom path to local and remote directories
read_args() {
    LDIR="${1:-$DEF_LOCAL_DIR}"
    RDIR="${2:-$DEF_REMOTE_DIR}"
}

#
remove_old() {
    echo "Removing old ${LIB} files..."
    delnet
}

#
copy_all() {
    echo "Copying files to remote host..."
    copy_testnet
#    copy_binaries
    echo
}

# Copy library files to VM
copy_testnet() {
    scp -r "${LDIR}" mininet@vm:"${RDIR}"
}

#
copy_binaries() {
    scp -r "${BUNDLE}/bin" mininet@vm:"~/bin"
}

# List all files in Remote Directory
list_dir() {
    echo "Listing ${LIB} directory contents:"
    ssh mininet@vm "ls ${RDIR}/*"
}

# Set executable privileges
set_privilege() {
    echo "Setting file access privilege..."
    
    ( ssh mininet@vm "chmod 0755 ${RDIR}/${MAIN_SCRIPT}" \
    && echo -e "\t${MAIN_SCRIPT}: 0755" )
    ( ssh mininet@vm "chmod 0755 ${RDIR}/${HELP_SCRIPT}" \
    && echo -e "\t${HELP_SCRIPT}: 0755" )
    
#    find "${LDIR}" -name "/${LIB}*.py" -exec 'echo -e "\t"{}": 0755"' \;
#    find "$LDIR/.." -path '*/TestNet/TestNet*.py' \
#        -exec sh -c 'echo "\t$(basename {}): \t 0755"' \;
#    ssh mininet@vm "chmod -v 0755 ${RDIR}/${MAIN_SCRIPT}"
#    ssh mininet@vm "chmod 0755 ${RDIR}/${LIB}*.py"
}

display_info() {
	echo -e "\nExecutable scripts:"
    echo -e "\t$(display_cmd ${LIB}/${MAIN_SCRIPT}): create a test network (run as root)."
    echo -e "\t$(display_cmd ${LIB}/${HELP_SCRIPT}): show help and view available commands."
}

display_broadcast() {
	MSG="Installing ${LIB} in ${DEF_REMOTE_DIR}."
#	ssh -o SendEnv=MSG mininet@vm "sudo wall -n '${MSG}'"
    echo -e "\t"$MSG | write $USER
}





# Install TestNet
__makenet__() {
    echo ">> Running $(display_cmd 'makenet') utility..."
    ( read_args \
    && remove_old \
    && copy_all \
    && set_privilege \
    && display_broadcast )
    
    display_info
    echo
#    && copy_binaries )
#    list_dir
}

# Usage:
#   'makenet' (default)
#   'makenet ~/local/TestNet ~/remote/TestNet'
__makenet__ "${1}" "${2}"
