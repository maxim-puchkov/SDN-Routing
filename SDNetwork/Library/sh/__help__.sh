#!/bin/sh

#  __help__.sh
#  Display TestNet help
#
#  Created by admin on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

HELP_SCRIPT="./TestNetHelp.py"


display_cmd() {
	tput setaf 5
	tput bold
	echo -n "${1}"
	tput sgr0
}

# Make executables of all .sh files and store them in SDNetwork/bin
__makesh__() {
    echo ">> Running $(display_cmd 'makesh') utility..."
    ( read_args \
    && compile_all \
    && display_stats )
}


__help__() {
    echo ">> Running $(display_cmd 'help') utility..."
    find . -path "*/TestNet/${HELP_SCRIPT}" \
        -exec sh -c 'echo "Found the mf: {}"' \;
}

#__help__

#python ${HELP_SCRIPT}

python Library/TestNet/TestNetHelp.py
