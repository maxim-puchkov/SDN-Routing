#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  main.py
#  Test Network main function
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.topo import Topo, LinearTopo
from TestNet.Topology import SuperTopo, SubnetTopo, LinkTopo, BabyTopo, TinyTopo, SmallTopo, LargeTopo



topos = {
    'baby': BabyTopo,
    'tiny': TinyTopo,
    'small': SmallTopo,
    'large': LargeTopo
}
