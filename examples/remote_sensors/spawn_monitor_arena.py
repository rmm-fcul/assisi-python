#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

the agents are spawned in a specifc environment/simulator, which can be a
remote machine -- although this canonical example uses the IP address of
`localhost`.

"""

from assisipy import sim
import argparse

from math import pi

if __name__ == "__main__":
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
    print "[I] attempting to connect a controller handle to server @"
    print "\t publish address =" + pub_addr
    simctrl = sim.Control(pub_addr=pub_addr)

    # Spawn casu (syntax is 'type', 'name', (x,y,yaw))
    #yaw = 0.0 # this points to the RIGHT
    yaw = pi/2 # this points UP
    #yaw = -pi/2 # this points down,
    simctrl.spawn('Casu','casu-monitor',  (+0,0, yaw))

