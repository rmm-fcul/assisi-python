#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool for remotely running CASU controllers.
"""

from fabric.api import settings, cd, run, env

import yaml

import os.path
import argparse
import threading

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

        # Running controllers
        self.running = {}

    def run_single(self,host,username,controller,rtc):
        """
        Run a single controller instance, on the specified host.

        controller - full path to the controller code
        rtc - full path or just file name (assumes it's in the same folder with the controller)
        """
        with settings(host_string = host, user = username):
            with cd(os.path.dirname(controller)):
                    run('export PYTHONPATH=/home/assisi/assisi-python:$PYTHONPATH;' + './' + os.path.basename(controller) + ' ' + rtc)

    def run(self):
        """
        Execute the controllers.
        """
        #env.parallel = True
        counter = 0
        for layer in self.depspec:
            for casu in self.depspec[layer]:
                ctrl_name = os.path.basename(self.depspec[layer][casu]['controller'])
                rtc_name = casu + '.rtc'
                args = (self.depspec[layer][casu]['hostname'],
                        self.depspec[layer][casu]['user'],
                        os.path.join(self.depspec[layer][casu]['prefix'],layer,casu,ctrl_name),
                        rtc_name)
                self.running[layer+'/'+casu] = threading.Thread(target=self.run_single,args=args)
                self.running[layer+'/'+casu].start()
                counter += 1
                if counter: break

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Run a set of CASU controllers.')
    parser.add_argument('depfile', help='name of .dep file specifying the deployment details.')
    args = parser.parse_args()

    project = Rundep(args.depfile)
    project.run()
