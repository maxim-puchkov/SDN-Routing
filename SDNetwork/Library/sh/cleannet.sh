#!/bin/sh

#  cleannet.sh
#  Clean up compiled source files in the TestNet folder
#
#  Created by admin on 2019-11-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.

DEF_REMOTE_DIR="~/TestNet"
DEL_EXT="pyc"

function __cleannet__() {
    echo ">> Running cleannet utility..."
    ssh mininet@vm "find ${DEF_REMOTE_DIR} -name "*.${DEL_EXT}" -exec rm -rfv {} \;"
    echo "Deleted all files with extension '.${DEL_EXT}'."
}

__cleannet__
