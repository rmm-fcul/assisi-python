#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple bee controller which makes the bee spin around
in place and report the object detected by its front proximity sensor.
"""

from assisipy import bee

import time

if __name__ == '__main__':

    b1 = bee.Bee(name='bee-001')
    b1.set_vel(-0.1,0.1)

    print('Press Ctrl-C to stop.')

    while True:
        (obj,r) = b1.get_object_with_range(bee.OBJECT_FRONT)
        print('Detected {0} at {1}cm ahead.'.format(obj,r))
        time.sleep(1)
