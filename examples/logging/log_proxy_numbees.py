#!/usr/bin/env python
# A program for logging proximity sensor values

import time
import argparse
import os

from assisipy import casu
from assisipy.tools import logtools

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Test casu heat actuator.")
    parser.add_argument('-rtc', '--rtc_file', help='Casu configuration file name.')
    parser.add_argument('-dir', '--log_directory', help='Logging directory.',
                        default='.')
    parser.add_argument('-nb', '--numbees', help='Number of bees in the arena.',
                        type=int, default=0)
    parser.add_argument('-d', '--duration', help='Experiment duration, in minutes.',
                        type=int, default=10)

    args = parser.parse_args()
    if args.log_directory[-1] != '/':
        args.log_directory += '/'

    print('Trying to connect to Casu...')
    mycasu = casu.Casu(args.rtc_file, log=True, log_folder=args.log_directory)
    
    #time_done = time.time() + args.duration * 60
    print('Experiment will be over in {0} minutes.'.format(args.duration))
    time.sleep(args.duration*60)
    
    mycasu.stop()

    # Process the log files
    logtools.split(mycasu.log_path)


    # Write the number of bees in the experiment
    path_list = mycasu.log_path.split('.')
    ir_raw_path = '-ir_raw.'.join(path_list)
    out_log_path = '-ir_raw-{0}-bees.'.format(args.numbees).join(path_list)
    with open(ir_raw_path) as in_logfile:
        with open(out_log_path,'wb') as out_logfile:
            out_logfile.writelines(['Number of bees: {0}\n'.format(args.numbees)])
            for line in in_logfile:
                out_logfile.writelines([line])

    # Clean up unnecessary logfiles
    all_files = os.listdir(args.log_directory)
    for csv_file in all_files:
        if csv_file.find('-bees') < 0:
            os.remove(args.log_directory + csv_file)

