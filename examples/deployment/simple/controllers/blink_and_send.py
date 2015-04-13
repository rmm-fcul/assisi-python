#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

import sys
import time

if __name__ == '__main__':

    c = casu.Casu(sys.argv[1])

    while True:
        c.set_diagnostic_led_rgb(r=1)
        time.sleep(1)
        c.set_diagnostic_led_rgb(r=0)
        time.sleep(1)
