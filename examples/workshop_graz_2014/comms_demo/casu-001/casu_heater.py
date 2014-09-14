#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from assisipy import casu


heating_temp = 40
cooling_temp = 15

if __name__ == '__main__':
    
    heatcasu = casu.Casu()
    
    while True:
        heatcasu.set_temp(heating_temp)
        sleep(5)



