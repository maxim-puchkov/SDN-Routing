#!/bin/sh

#  ShellCompiler.sh
#  Compile shell scripts and save executables in the project's binary folder
#
#  Created by admin on 2019-11-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

BUNDLE_DIR="/Users/admin/Developer/Projects/macOS/SDNetwork/SDNetwork"
EXECUTABLE_DISPLAY_NAME="ShellCompiler"
export COMPILER_DISPLAY_NAME="makesh"
export EXT="sh"

# Full path to script directory (default)
DEF_SCRIPT_DIR="${BUNDLE_DIR}/Library/sh"
# Full binary output path (default)
DEF_BINARY_DIR="${BUNDLE_DIR}/bin"


display_cmd() {
	tput setaf 5
	tput bold
	echo -n "${1}"
	tput sgr0
}

# Read custom path to script directory
read_args() {
    export SDIR="${1:-$DEF_SCRIPT_DIR}"
    export BDIR="${1:-$DEF_BINARY_DIR}"
}

display_compile_stats() {
    COUNT=$(echo $(find "${SDIR}" \
                    -name "*.${EXT}" \
                    -not -name "${EXECUTABLE_DISPLAY_NAME}.${EXT}" | wc -l))
    echo -e "\tCompiled ${COUNT} shell scripts."
}

display_update_stats() {
    echo -e "\tUpdated the compiler."
}

display_stats() {
    echo "ShellCompiler:"
    display_compile_stats
    display_update_stats
    echo -e "\nTo run the compiler again, run the" \
            "$(display_cmd $COMPILER_DISPLAY_NAME) utility."
}

# Compile all other shells
compile_shells() {
    echo -e "\tCompiling shells:"
    find "${SDIR}" \
        -name "*.${EXT}" \
        -not -name "${EXECUTABLE_DISPLAY_NAME}.${EXT}" \
        -exec sh -c 'BASE=$(basename {} ".${EXT}") \
                    && echo "\t\t${BASE}...\c" \
                    && shc -o "${BDIR}/${BASE}" -f "${SDIR}/${BASE}.${EXT}" \
                    && echo " done."' \;
    mv "${BDIR}/__help__" "${BDIR}/../help"
    echo
}

# 'Recompile' the compiler
update_compiler() {
    updateshc
}

# Compile all .sh scripts
compile_all() {
    ( compile_shells \
    && update_compiler )
}






# Make executables of all .sh files and store them in SDNetwork/bin
__makesh__() {
    echo ">> Running $(display_cmd 'makesh') utility..."
    ( read_args \
    && compile_all \
    && display_stats )
    echo
}

# Usage:
#   'makesh' (default)
#   'makesh input/path/sh output/path/bin'
__makesh__ "${1}" "${2}"

# Other commands:
#   'makenet' - remove old files and reinstall TestNet on VM
#   'delnet'  - remove TestNet from VM
#   'help'    - show help
