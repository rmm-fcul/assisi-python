#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A simple demo of bee-casu interaction, with bees rotating about
# CASUs to periodically trigger IR sensors.

from assisipy import bee
import time

import argparse
#import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-svr', '--server-addr', type=str, default='127.0.0.1',
                        help="the IP address of the enki server")
    parser.add_argument('-pp', '--pub-port', type=str, default='5556',
                        help="publish port (wherever the enki server listens for commands)")
    parser.add_argument('-sp', '--sub-port', type=str, default='5555',
                        help="subscribe port (wherever the enki server emits commands)")
    args = parser.parse_args()

    pub_addr = "tcp://{}:{}".format(args.server_addr, args.pub_port)
    sub_addr = "tcp://{}:{}".format(args.server_addr, args.sub_port)
    # Connect to the bee
    walkers = []
    names = ['Bee-001', 'Bee-002']
    walkers = [
        bee.Bee(name=n, pub_addr=pub_addr, sub_addr=sub_addr)
        for n in names]

    # Let the bee run in circles
    for i, w in enumerate(walkers):
        f = (i+1) * 1.0 # growth rate

        w.set_vel(f*0.65, f*0.8)

    try:
        #print "[I] my PID is: ", os.getpid()
        while True:
            time.sleep(3.5)
            pass
    except KeyboardInterrupt:
        print "shutting down bees..."
        for w in walkers:
            w.set_vel(0, 0)









