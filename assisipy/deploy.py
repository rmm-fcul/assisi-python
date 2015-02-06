#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pygraphviz as pgv

import sys
import os
import shutil

""" Tools for automatically deploying CASU controllers. """

class Deploy:
    """
    Class for performing deployment tasks.

    Parses the configuration files and initializes internal data structures.

    :param arena_file_name: Name of the .arena arena configuration file.
    :param nbg_file_name: Name of the .nbg neighborhood graph file.
    :param dep_file_name: Name of the .dep dependency specificaton file.
    """

    def __init__(self, project_file_name):
 
        self.arena = {}
        self.nbg = {}
        self.dep = {}

        self.project_root = os.path.dirname(os.path.abspath(project_file_name))
        self.sandbox_dir = project_file_name.split('.')[0] + '_deploy'

        with open(project_file_name) as project_file:
            project = yaml.safe_load(project_file)
            
        with open(os.path.join(self.project_root, project['arena'])) as arena_file:
            self.arena = yaml.safe_load(arena_file)

        self.nbg = pgv.AGraph(os.path.join(self.project_root, project['nbg']))

    def prepare(self):
        """
        Prepare deployment in local folder.
        """

        cwd = os.getcwd()
        print('Changing directory to {0}'.format(self.project_root))
        os.chdir(self.project_root)
        print('Preparing files for deployment!')

        # Clean up and create new sandbox folder
        sandbox_path = os.path.join(self.project_root, self.sandbox_dir)
        print('The folder {0} will be overwritten!'.format(sandbox_path))
        try:
            shutil.rmtree(sandbox_path)
        except OSError:
            # The sandbox directory does not exist,
            # no biggie
            pass
        
        # Create one folder per arena layer
        # with subfolders for each casu
        os.mkdir(self.sandbox_dir)
        os.chdir(self.sandbox_dir)
        for layer in self.arena:
            os.mkdir(layer)
            os.chdir(layer)
            for casu in self.arena[layer]:
                os.mkdir(casu)
                os.chdir(casu)
                with open(casu+'.rtc','a') as rtc_file:
                    yaml.dump({'name':casu}, rtc_file, default_flow_style=False)
                    yaml.dump({'pub_addr': self.arena[layer][casu]['pub_addr']},
                               rtc_file, default_flow_style=False)
                    yaml.dump({'sub_addr': self.arena[layer][casu]['sub_addr']},
                              rtc_file, default_flow_style=False)
                    yaml.dump({'msg_addr': self.arena[layer][casu]['msg_addr']}, 
                              rtc_file, default_flow_style=False)
                    neighbors = {'neighbors':{}}
                    for nb in self.nbg.out_neighbors(casu):
                        neighbors['neighbors'][str(nb)] = 'test'
                    yaml.dump(neighbors, rtc_file, default_flow_style=False)

                os.chdir('..')
            os.chdir(sandbox_path)
        

        print('Returning to original directory {0}'.format(cwd))

if __name__ == '__main__':

    # TODO: use argparse!

    deploy = Deploy(sys.argv[1])
    deploy.prepare()

