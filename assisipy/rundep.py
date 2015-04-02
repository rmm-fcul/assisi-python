#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool for remotely running CASU controllers.
"""

import yaml

import sys

class Rundep:
    """
    Remote execution tool.
    """
    def __init__(self, depfile_name):
        """
        Constructor.
        """
        self.depspec = {}
        with open(depfile_name) as depfile:
            self.depspec = yaml.safe_load(depfile)

    def run(self):
        """
        Execute the controllers.
        """
        for arena in self.depspec:
            for casu in self.depspec[arena]:
                pass

if __name__ == '__main__':
    
    # TODO: Use argparse
    project = Rundep(sys.argv[1])
    project.run()
