#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Identical wander controllers for 36 bees.
"""

from assisipy import bee

from math import pi, sin, cos
from random import random
import threading

class BeeWander:
    """ 
    A demo bee wander controller. 
    An example of using the Bee-API.
    """

    def __init__(self, bee_name):
        self.__bee = bee.Bee(name = bee_name)
        self.__thread = threading.Thread(target=self.wander)
        self.__thread.daemon = True
        self.__thread.start()

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

    num_bees = 36

    # Spawn the bees at randomly generated poses and let them run :)
    bees = []
    for i in range(1,num_bees+1):
        if i < 10:
            bees.append(BeeWander('Bee-00{0}'.format(i)))
        else:
            bees.append(BeeWander('Bee-0{0}'.format(i)))

    print('All bees connected!')

    # Prevent the program from exiting
    while True:
        pass

        
