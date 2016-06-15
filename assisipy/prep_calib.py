#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A tool to generate new specifications from the existing spec, solely for
calibration stage.

This works locally, creating a sandbox

'''

import yaml
#from fabric.api import run, put, settings

import argparse
import os
import shutil


class PrepCalib(object):
    """
    Class that generates .dep files and sandboxes for calibration
    """

    def __init__(self, project_file_name):
        """
        Parses the configuration files and initializes internal data structures.
        """
        self.proj_name = os.path.splitext(os.path.basename(project_file_name))[0]
        self.fabfile_name = self.proj_name + '.py'
        self.arena = {}
        self.dep = {}

        self.project_root = os.path.dirname(os.path.abspath(project_file_name))
        self.sandbox_dir = self.proj_name + '_calib' + '_sandbox'


        self.prepared = False

        with open(project_file_name) as project_file:
            self.project = yaml.safe_load(project_file)

        # Read the .arena file
        with open(os.path.join(self.project_root, self.project['arena'])) as arena_file:
            self.arena = yaml.safe_load(arena_file)

        # Read the deployment file
        with open(os.path.join(self.project_root, self.project['dep'])) as dep_file:
            self.dep = yaml.safe_load(dep_file)

        self.out_project_file = "calib_" + self.proj_name + '.assisi'
        self.out_dep_file     = "calib_" + self.project['dep']


    def prep(self):
        self.prep_calib()
        self.prep_main()

    def prep_main(self):
        pass

    def prep_calib(self):
        '''
        prepare the calibration code in local folder
        '''
        cwd = os.getcwd()
        print('Changing directory to {0}'.format(self.project_root))
        os.chdir(self.project_root)
        print('Preparing !')

        # Clean up and create new sandbox folder
        sandbox_path = os.path.join(self.project_root, self.sandbox_dir)
        _msg = "created"
        if os.path.exists(sandbox_path):
            _msg = "overwritten"
        print("The folder \n\t{}\n will be {}".format(sandbox_path, _msg))
        try:
            shutil.rmtree(sandbox_path)
        except OSError:
            # The sandbox directory does not exist,
            # no biggie
            pass

        os.mkdir(self.sandbox_dir)
        os.chdir(self.sandbox_dir)


        # construct a new deployment file, with entries only for CASUs with
        # a calibration entry
        calib_dep = {}
        for layer in self.arena:
            calib_dep[layer] = {}
            for casu in self.arena[layer]:
                # find the basic deployment info
                depdata = self.dep[layer][casu]
                # and more proc if there is present a non-empty? calibration subdict,
                calibdata = depdata.get('calibration')
                #print casu, calibdata
                if calibdata is None:
                    print "[I] skipping {} {}".format(layer, casu)
                    continue

                calibdepinfo = {}
                for k in [ 'hostname', 'user', 'prefix' ]:
                    calibdepinfo[k] = depdata[k] # fail if not defined

                # lets now add the custom stuff that needs translation
                calibfile = calibdata['calibfile']

                calibdepinfo['controller'] = calibdata['controller']
                calibdepinfo['output']     = calibdata.get('output', []) + [calibfile]
                calibdepinfo['extra']      = calibdata.get('extra', [])  + ["--output", calibfile]

                print "[I] constructed new deployment info for {}".format(casu)
                print calibdepinfo


                calib_dep[layer][casu] = calibdepinfo

                #

        sd = yaml.safe_dump(calib_dep, default_flow_style=False)
        with open(self.out_dep_file, 'w')  as outdep:
            outdep.write(sd + "\n")

        # now do the project file
        calibproj = dict(self.project)
        # just update the .dep file
        calibproj['dep'] = self.out_dep_file

        sp = yaml.safe_dump(calibproj, default_flow_style=False)
        with open(self.out_project_file, 'w')  as outproj:
            outproj.write(sp + "\n")


        # finally, copy the .arena and .nbg files to the sandbox.
        dst = os.path.join(self.project_root, self.sandbox_dir)
        src = os.path.join(self.project_root, calibproj['arena'])
        #print "src to dest: \n\t{} \n\t{}".format(src, dst)
        shutil.copy2(src, dst)
        src = os.path.join(self.project_root, calibproj['nbg'])
        #print "src to dest: \n\t{} \n\t{}".format(src, dst)
        shutil.copy2(src, dst)

        print('Returning to original directory {0}'.format(cwd))
        os.chdir(cwd)

        self.prepared = True


def main():
    parser = argparse.ArgumentParser(description='Transfer controller code to CASUs (physical or simulated)')
    parser = argparse.ArgumentParser(description='Generate a deployment setup for calibration of CASUs')
    parser.add_argument('project', help='name of .assisi file specifying the project details.')
    # TODO: This is fully implemented yet!
    parser.add_argument('--layer', help='Name of single layer to action', default='all')
    args = parser.parse_args()

    project = PrepCalib(args.project)
    project.prep()

if __name__ == '__main__':
    main()
