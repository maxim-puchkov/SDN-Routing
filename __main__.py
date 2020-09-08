#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  __main__.py
#  Test Network main function
#
#  Created by mpuchkov on 2019-12-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

import sys
from run import __run__ as run_demo


# Main function
if __name__ == '__main__':
    argc = len( sys.argv )
    run_demo( argc, sys.argv )
