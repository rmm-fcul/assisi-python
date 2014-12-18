#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple bee wander behavior, spawned in an arbitrary environment/simulator.

The bee behaviour is taken directly from examples/wandering_bee.

"""

import argparse
from assisipy import bee

class BeeWander:
    """
    A demo bee controller.
    An simple example of using the Bee-API.
    """

    def __init__(self, bee_name, pub_addr, sub_addr):
        # note: this connection only works with the `config_agents` branch of
        # RMM-FCUL fork
        self.__bee = bee.Bee(name=bee_name, pub_addr=pub_addr, sub_addr=sub_addr)

    def go_straight(self):
        self.__bee.set_vel(0.5,0.5)

    def stop(self):
        self.__bee.set_vel(0.,0.)

    def turn_left(self):
        self.__bee.set_vel(-0.1,0.1)

    def turn_right(self):
        self.__bee.set_vel(0.1,-0.1)

    def wander(self):
        """
        Wander around and avoid obstacles.
        """
        while True:
            self.go_straight()
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_RIGHT_FRONT) < 4)):
                self.turn_left()
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_LEFT_FRONT) < 4)):
                self.turn_right()

if __name__ == '__main__':
    # process command-line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-bn', '--bee-name', type=str, default='bee-001',
                        help="name of the bee to attach to")
    parser.add_argument('-svr', '--server-addr', type=str, default='127.0.0.1',
                        help="the IP address of the enki server")
    parser.add_argument('-pp', '--pub-port', type=str, default='5556',
                        help="publish port (wherever the enki server listens for commands)")
    parser.add_argument('-sp', '--sub-port', type=str, default='5555',
                        help="subscribe port (wherever the enki server emits commands)")
    args = parser.parse_args()


    pub_addr = "tcp://{}:{}".format(args.server_addr, args.pub_port)
    sub_addr = "tcp://{}:{}".format(args.server_addr, args.sub_port)
    # Start the wander behavior.
    # The name has to match the name of the spawned bee!
    wanderer = BeeWander(bee_name=args.bee_name, pub_addr=pub_addr,
                         sub_addr=sub_addr,)

    # start behaviour, and handle keyboard interrupt gracefully
    try:
        wanderer.wander()
    except KeyboardInterrupt:
        print "shutting down bee {}".format(args.bee_name)

    wanderer.stop()
