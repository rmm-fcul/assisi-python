#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from assisipy import casu


heating_temp = 40
cooling_temp = 15

if __name__ == '__main__':
    
    senscasu = casu.Casu()
    
    while True:
        print('N: {0}, S: {1}, E: {2}, W: {3}, T: {4}'.format(senscasu.get_temp(casu.TEMP_N),
                                                      senscasu.get_temp(casu.TEMP_S),
                                                      senscasu.get_temp(casu.TEMP_E),
                                                      senscasu.get_temp(casu.TEMP_W),
                                                      senscasu.get_temp(casu.TEMP_TOP)))
        sleep(5)

