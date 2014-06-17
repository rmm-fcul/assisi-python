#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple bee wander behavior.
"""

from assisipy import bee

class BeeWander:
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
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_RIGHT_FRONT) < 4)):
                self.turn_left()
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_LEFT_FRONT) < 4)):
                self.turn_right()

if __name__ == '__main__':
    
    # Start the wander behavior.
    # The name has to match the name of the spawned bee!
    wanderer = BeeWander('bee1')
    wanderer.wander()

