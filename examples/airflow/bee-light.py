#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple bee that measures air flow.
"""

from assisipy import bee
import random
import math
from time import sleep

class BeeWander:
    """ 
    A wandering bee that measures air flow.
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
            if ((self.__bee.get_range (bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range (bee.OBJECT_RIGHT_FRONT) < 4)):
                self.turn_left ()
            elif ((self.__bee.get_range (bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range (bee.OBJECT_LEFT_FRONT) < 4)):
                self.turn_right()
            else:
                action = random.random ()
                if action < 0.4:
                    self.turn_left ()
                elif action < 0.8:
                    self.turn_right ()
                else:
                    self.go_straight()
            airflow_intensity = self.__bee.get_airflow_intensity ()
            airflow_angle = self.__bee.get_airflow_direction ()
            if airflow_intensity > 0:
                (_,_,pose) = self.__bee.get_true_pose ()
                print ('my heading {:4.0f}º    airflow from {:4.0f}º at {:5.2f}l/s'.format (
                    pose * 180 / math.pi,
                    airflow_angle * 180 / math.pi,
                    airflow_intensity))
            sleep (0.2)

class BeeStraight:
    """ 
    A bee that walks in a straight line while measuring air flow.
    """

    def __init__(self, bee_name):
        self.__bee = bee.Bee(name = bee_name)

    def go_straight(self):
        self.__bee.set_vel(0.5,0.5)

    def turn_left(self):
        self.__bee.set_vel(-0.1,0.1)

    def turn_right(self):
        self.__bee.set_vel(0.1,-0.1)

    def main_loop(self):
        """ 
        Walk in a straight line avoid obstacles. 
        """
        while True:
            if ((self.__bee.get_range (bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range (bee.OBJECT_RIGHT_FRONT) < 4)):
                self.turn_left ()
            elif ((self.__bee.get_range (bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range (bee.OBJECT_LEFT_FRONT) < 4)):
                self.turn_right()
            else:
                self.go_straight()
            airflow_intensity = self.__bee.get_airflow_intensity ()
            airflow_angle = self.__bee.get_airflow_direction ()
            if airflow_intensity > 0:
                (_,_,pose) = self.__bee.get_true_pose ()
                print ('my heading {:4.0f}º    airflow from {:4.0f}º at {:5.2f}l/s'.format (
                    pose * 180 / math.pi,
                    airflow_angle * 180 / math.pi,
                    airflow_intensity))
            sleep (0.2)

if __name__ == '__main__':
    
    # Start the behavior.
    # The name has to match the name of the spawned bee!
    #wanderer = BeeWander('bee1')
    #wanderer.wander()

    mybee = BeeStraight('bee1')
    mybee.main_loop()

