#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from assisipy import casu


max_temp = 32
min_temp = 28

if __name__ == '__main__':
    
    senscasu = casu.Casu()
    
    while True:
        temp = senscasu.get_temp(casu.TEMP_E)
        print('Temperature on EAST sensor: {0}'.format(temp));
        if temp > max_temp:
            senscasu.send_message('east','Cool down!')
            print('Temperature too hot!')
        elif temp < min_temp:
            senscasu.send_message('east','Warm up!')
            print('Temperature too low!')
        sleep(5)

