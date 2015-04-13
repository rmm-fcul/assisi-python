#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
a simple simulation environment with one casu and one bee.

the agents are spawned in a specifc environment/simulator, which can be a
remote machine -- although this canonical example uses the IP address of
`localhost`.


'''

import argparse
from assisipy import sim


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

    # spawn casu and bee into the simulator
    # (type, name, coordinaets)
    # coordinates: x,y,orientation(rad)
    casu_name = 'casu-001'
    bee_name  = 'bee-001'
    simctrl.spawn('Casu', casu_name, (0,0,0))
    print "[I] spawn of Casu '{}' requested".format(casu_name)
    simctrl.spawn('Bee', bee_name, (3,5,0))
    print "[I] spawn of Bee  '{}' requested".format(bee_name)


