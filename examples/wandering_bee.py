#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple demo app demonstrating the "Wander" behavior with a bee model
"""

from assisipy import sim
from assisipy import physical
from assisipy import bee

from math import pi

class BeeController:
    """ 
    A demo bee controller. 
    An simple example of using the Bee-API.
    """

    def __init__(self, bee_name):
        self.__bee = bee.Bee(name = bee_name)

    def go_straight(self):
        self.__bee.set_vel(0.5,0.5)

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
            while ((self.__bee.get_range(bee.IR_FRONT) < 3)
                   and (self.__bee.get_range(bee.IR_RIGHT_FRONT) < 4)):
                self.turn_left()
            while ((self.__bee.get_range(bee.IR_FRONT) < 3)
                   and (self.__bee.get_range(bee.IR_LEFT_FRONT) < 4)):
                self.turn_right()

if __name__ == '__main__':
    
    simctrl = sim.Control()

    # Spawn some obstacles into the world.
    l = 5
    w = 2
    wall = ((-l,-w/2),(l,-w/2),(l,w/2),(-l,w/2))
    blue = (0,0,1)
    simctrl.spawn('Physical', 'wall1', (0,-6,0), 
                  polygon = wall,
                  color = blue, height = 1)

    simctrl.spawn('Physical', 'wall2', (5,-1,pi/2), 
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall3', (5,7,0),
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall4', (15,7,pi/2),
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall5', (-7,9,pi/2),
                  polygon = wall,
                  color = blue, height = 1)

    # Spawn the bee.
    simctrl.spawn('Bee', 'bee1', (0,0,0))
    bc = BeeController('bee1')
    
    # Start the wander behavior.
    bc.wander()

