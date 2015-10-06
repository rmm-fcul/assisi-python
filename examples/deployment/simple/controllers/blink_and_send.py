#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Blinking CASU behavior.
Waits for message from any neighbors.
When a message arrives, blinks it's LED and forwards
the message.

Optional argument sets the LED channel that will be active.
(v. simple parsing only works for strings r,g,b; it is intended
 to demonstrate `extra_args` in dep files & not LEDs per se)
"""

from assisipy import casu

import sys
import time

if __name__ == '__main__':

    c = casu.Casu(sys.argv[1], log=True)
    # look for color specification in extra cmd-line arg.
    LED_colors = [1, 0, 0]
    if len(sys.argv)>2:
        _defn = sys.argv[2]
        LED_colors = [0, 0, 0]
        if 'r' in _defn: LED_colors[0] = 1
        if 'g' in _defn: LED_colors[1] = 1
        if 'b' in _defn: LED_colors[2] = 1



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
        c.set_diagnostic_led_rgb(*LED_colors)
        time.sleep(1)
        c.set_diagnostic_led_rgb(r=0, g=0, b=0)
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
