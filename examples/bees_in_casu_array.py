# A demo of bee casu interaction featuring 36 casus and 24 bees.

from assisipy import sim, bee, casu

from math import pi, sin, cos
from random import random
import threading

class CasuController:
    """ A demo Casu controller.
        Implements a simple bee-detecting behavior.
    """

    def __init__(self, casu_name):
        self.__casu = casu.Casu(name = casu_name)
        self.__thread = threading.Thread(target=self.react_to_bees)
        self.__thread.daemon = True
        self.__thread.start()

    def react_to_bees(self):
        """ 
            Changes Casu color to red, when a bee is detected in front of the Casu,
            and to Green, when a bee is detected behind a Casu.
        """
        while True:
            if self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
            elif self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 1, 0)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)

class BeeController:
    """ A demo bee controller. 
        This is only an example of using the Bee-API.
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
        """ Wander around and avoid obstacles. """
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

    casu_rows = 6
    casu_cols = 6
    casu_dist = 10
    num_bees = 24

    # Spawn the Casus and run their controllers
    casus = []
    x = range(-int(casu_dist*casu_cols/2), int(casu_dist*(casu_cols+1)/2), casu_dist)
    y = range(-int(casu_dist*casu_rows/2), int(casu_dist*(casu_rows+1)/2), casu_dist)
    for i in range(casu_rows):
        for j in range(casu_cols):
            simctrl.spawn('Casu', 'casu{0}{1}'.format(i,j), (x[i],y[j],0))
            casus.append(CasuController('casu{0}{1}'.format(i,j)))
    
    # Spawn the bees at randomly generated poses and let them run :)
    bees = []
    for i in range(num_bees):
        d = 38*random()
        a = 2*pi*random()
        simctrl.spawn('Bee', 'bee{0}'.format(i), (d*cos(a), d*sin(a), a))
        bees.append(BeeController('bee{0}'.format(i)))

    # Prevent the program from exiting
    while True:
        pass

        
