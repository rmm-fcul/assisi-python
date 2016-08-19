#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools for loading data from CASU logfiles.
"""

import sys
import os
import csv

import scipy.io as sio

def load_from_csv(filepath):
    """
    Load log data from a csv file.
    """
    data = {}

    filename = os.path.basename(filepath)
    casu = ''
    if len(filename) < 25:
        sys.exit('{0} is an invalid CASU log file name!.'.format(filename))
    else:
        casu = filename[20:-4].replace('-','_')
        data[casu] = {}

    with open(filepath) as datafile:
        datareader = csv.reader(datafile,delimiter=';')
        dataid = None
        for row in datareader:
            if len(row) > 2:
                # Guard against incomplete rows
                # (e.g. interrupted program)
                dataid = row[0].replace('-','_')
                t_id = 't_' + dataid
                ts = float(row[1]) # timestamp
                if dataid not in data[casu]:
                    # New row id
                    data[casu][dataid] = []
                    data[casu][t_id] = []
                data[casu][t_id].append(ts)
                try:
                    data[casu][dataid].append([float(x) for x in row[2:]])
                except ValueError:
                    #print('No data for {0}'.format(dataid))
                    # Accelerometers are currently not providing any data
                    # We don't want to bother users with that
                    pass

        # Check final row (my be incomplete)
        if dataid:
            # Some data were present
            if len(data[casu][dataid]) > 1:
                # At least two rows were present
                if not len(data[casu][dataid][-1]) == len(data[casu][dataid][-2]):
                    # Remove last row if it's incomplete
                    data[casu][dataid] = data[casu][dataid][:-1]

    return data

def process_folder(foldername):
    """
    Recurse into subfolders and process all csv files.
    """
    data = {}

    return data

def main():
    """
    Main script entry point.
    """
    # TODO: Use argparse and add reasonable options
    # Document usage
    # Consider if the program should take an .assisi file as input?

    data = {}
    
    # The first argument is the name
    # of the file/folder to process
    if len(sys.argv) < 2:
        sys.exit('Please provide a file or folder to process.')
    elif sys.argv[1][-4:] == '.csv':
        # We are assuming that we need to process a single .csv file
        data = load_from_csv(sys.argv[1])
    else:
        # We are assuming that the argument is a folder
        # to be processed. It is assumed that it contains
        # subfolders, each of which corresponds to one CASU.
        # Each subfolder is assumed to contain one or more
        # .csv files.
        data = process_folder(sys.argv[1])

    sio.savemat(sys.argv[1][:-4],data,oned_as='column')


if __name__ == '__main__':

    main()
