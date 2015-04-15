#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Blinking CASU behavior.
Waits for message from any neighbors.
When a message arrives, blinks it's LED and forwards 
the message.
"""

from assisipy import casu

import sys
import time

if __name__ == '__main__':

    c = casu.Casu(sys.argv[1], log=True)

    counter = 0
    while True:
        msg = c.read_message()
        while not msg:
            msg = c.read_message()

        # Message received
        # We are interested only in the first message
        # so empty the buffer
        while c.read_message():
            c.read_message()

        # Blink
        c.set_diagnostic_led_rgb(r=1)
        time.sleep(1)
        c.set_diagnostic_led_rgb(r=0)
        time.sleep(1)

        # Forward message
        c.send_message('front',msg['data'])
        c.send_message('right',msg['data'])
        c.send_message('back',msg['data'])
        c.send_message('left',msg['data'])

        # Sleep and empty message buffer,
        # to prevent message back-propagation
        time.sleep(3)
        while c.read_message():
            c.read_message()
