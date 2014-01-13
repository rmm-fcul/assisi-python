# A simple demo of bee-casu interaction

from assisipy import sim
from assisipy import bee
from assisipy import casu

from math import pi

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Bee and the Casu
    simctrl.spawn('Casu','casu1',(0,0,0))
    simctrl.spawn('Bee','bee1',(2,0,pi/2))

    casu1 = casu.Casu(name='casu1')
    bee1 = bee.Bee(name='bee1')
    
    # Let the bee run in circles
    bee1.set_vel(0.65,0.8)
    
    # React to bee position
    while True:
        if casu1.get_range(casu.IR_N) < 2:
            casu1.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
        elif casu1.get_range(casu.IR_S) < 2:
            casu1.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 1, 0)
        else:
            casu1.diagnostic_led_standby(casu.DLED_TOP)

            

    
