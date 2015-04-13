#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pygraphviz as pgv
from fabric.api import run, put, settings

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
 
        self.fabfile_name = project_file_name[:-7] + '.py'
        self.arena = {}
        self.nbg = {}
        self.dep = {}

        self.project_root = os.path.dirname(os.path.abspath(project_file_name))
        self.sandbox_dir = project_file_name.split('.')[0] + '_sandbox'

        self.prepared = False

        with open(project_file_name) as project_file:
            project = yaml.safe_load(project_file)
            
        # Read the .arena file
        with open(os.path.join(self.project_root, project['arena'])) as arena_file:
            self.arena = yaml.safe_load(arena_file)

        # Read the neighborhood graph
        self.nbg = pgv.AGraph(os.path.join(self.project_root, project['nbg']))

        # Read the deployment file
        with open(os.path.join(self.project_root, project['dep'])) as dep_file:
            self.dep = yaml.safe_load(dep_file)

    def prepare(self):
        """
        Prepare deployment in local folder.
        """

        cwd = os.getcwd()
        print('Changing directory to {0}'.format(self.project_root))
        os.chdir(self.project_root)
        print('Preparing files for deployment!')

        # Remove old fabfile, if it exists
        print('The file {0} will be overwritten!'.format(self.fabfile_name))
        try:
            os.remove(self.fabfile_name)
        except OSError:
            # The fabfile does not exist,
            # no bigie
            pass

        # Collect fabric tasks
        fabfile_tasks = '''
from fabric.api import cd, run, settings, parallel
'''
        fabfile_all = '''
def all():
'''

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
                # Create the .rtc file
                with open(casu+'.rtc','a') as rtc_file:
                    yaml.dump({'name':casu}, rtc_file, default_flow_style=False)
                    yaml.dump({'pub_addr': self.arena[layer][casu]['pub_addr']},
                               rtc_file, default_flow_style=False)
                    yaml.dump({'sub_addr': self.arena[layer][casu]['sub_addr']},
                              rtc_file, default_flow_style=False)
                    yaml.dump({'msg_addr': 'tcp://*:' + self.arena[layer][casu]['msg_addr'].split(':')[-1]}, 
                              rtc_file, default_flow_style=False)
                    neighbors = {'neighbors':{}}
                    for nb in self.nbg.get_subgraph(layer).out_neighbors(casu):
                        side = str(self.nbg.get_edge(casu,nb).attr['label'])
                        nb_full_name = str(nb).split('/')
                        nb_name = nb_full_name[-1]
                        nb_layer = layer
                        if len(nb_full_name) > 1:
                            nb_layer = nb_full_name[0]
                        neighbors['neighbors'][side] = {'name': nb_name,
                                                        'address': self.arena[nb_layer][nb_name]['msg_addr']}
                    yaml.dump(neighbors, rtc_file, default_flow_style=False)

                # Copy the controller
                shutil.copy(os.path.join(self.project_root,self.dep[layer][casu]['controller']),'.')

                # Append to fabfile
                fabfile_tasks += '''
@parallel
def {task}():
    with settings(host_string='{host}', user='{username}'):
        with cd('{code_dir}'):
                run('export PYTHONPATH=/home/assisi/python:$PYTHONPATH; ./{command} {rtc}')
                                  '''.format(task=(layer+'_'+casu).replace('-','_'),
                                             host=self.dep[layer][casu]['hostname'],
                                             username=self.dep[layer][casu]['user'],
                                             code_dir=os.path.join(self.dep[layer][casu]['prefix'],layer,casu),
                                             command=os.path.basename(self.dep[layer][casu]['controller']),
                                             rtc=casu+'.rtc')
                fabfile_all += '    {task}()\n'.format(task=(layer+'_'+casu).replace('-','_'))
                os.chdir('..')
            os.chdir(sandbox_path)
        
        os.chdir(self.project_root)

        # Finalize the fabric file
        with open(self.fabfile_name,'w') as fabfile:
            fabfile.write(fabfile_tasks)
            fabfile.write(fabfile_all)

        print('Preparaton done!')
        print('Returning to original directory {0}'.format(cwd))
        os.chdir(cwd)
        
        self.prepared = True

    def deploy(self):
        """ 
        Perform deployment by copying files from the sandbox directory
        to their appropriate destinations.
        """
        
        if not self.prepared:
            self.prepare()

        cwd = os.getcwd()

        os.chdir(os.path.join(self.project_root, self.sandbox_dir))
        for layer in self.dep:
            print('Deploying layer {0} ...'.format(layer))
            os.chdir(layer)
            for casu in self.dep[layer]:
                os.chdir(casu)
                # Connect to the target machine and deploy the files.
                with settings(host_string = self.dep[layer][casu]['hostname'],
                              user = self.dep[layer][casu]['user']):
                    destdir = os.path.join(self.dep[layer][casu]['prefix'], layer, casu)
                    run('mkdir -p ' + destdir)
                    run('rm -rf ' + os.path.join(destdir,'*'))
                    put('*', destdir)
                    # Give executable permissions to the controller
                    ctrl_name = os.path.basename(self.dep[layer][casu]['controller'])
                    run('chmod +x ' + os.path.join(destdir, ctrl_name))
                os.chdir('..')
            os.chdir('..')
        
        os.chdir(cwd)

if __name__ == '__main__':

    # TODO: use argparse!
    project = Deploy(sys.argv[1])
    project.deploy()
