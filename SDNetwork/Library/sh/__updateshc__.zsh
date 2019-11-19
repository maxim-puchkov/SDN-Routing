#!/bin/zsh

#  __update__.zsh
#  Update ShellCompiler.sh 
#
#  Created by admin on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.


BUNDLE_DIR="/Users/admin/Developer/Projects/macOS/SDNetwork/SDNetwork"
BINARY_DISPLAY_NAME="updateshc"
COMPILER_SOURCE="ShellCompiler"
export SDIR="${BUNDLE_DIR}/Library/sh"
export BDIR="${BUNDLE_DIR}/bin"

export COMPILER_DISPLAY_NAME="makesh"
export EXT="sh"


display_cmd() {
	tput setaf 5
	tput bold
	/bin/echo -n "${1}"
	tput sgr0
}


update_self() {
    shc -o "${BDIR}/${BINARY_DISPLAY_NAME}" -f "${SDIR}/__${BINARY_DISPLAY_NAME}__.zsh"
}



# 'Recompile' the compiler
update_compiler() {
    echo -e "\tUpdating ${COMPILER_SOURCE}:"
    find "${SDIR}" \
        -name "*${COMPILER_SOURCE}.${EXT}" \
        -exec sh -c 'BASE=$(basename {} ".${EXT}") \
                    && echo "\t\t${COMPILER_DISPLAY_NAME}... \c" \
                    && shc -o "${BDIR}/${COMPILER_DISPLAY_NAME}" -f "${SDIR}/${BASE}.${EXT}" \
                    && echo "done."' \;
}





# Make executables of all .sh files and store them in SDNetwork/bin
__updateshc__() {
    echo ">> Running $(display_cmd 'updateshc') utility..."
    update_self
	update_compiler
    echo
}


# Usage:
#   1. Run the script to generate 'makesh' binary executable:
#       ./__update2__.sh
#   2. Export the path in ~/.profile:
#       TESTNET_BIN_PATH="$HOME/bin"
#       export PATH=$PATH:$TESTNET_BIN_PATH
#   3. Run 'makesh' command to compile shell scripts.
#       makesh
__updateshc__
