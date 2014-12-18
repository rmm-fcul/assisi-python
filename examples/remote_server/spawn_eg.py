#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
eg 1

a simple simulation environment with one casu and one bee.


'''

from assisipy import sim


if __name__ == "__main__":
        simctrl = sim.Control()
        remote_svr = "tcp://127.0.01"
        pub_addr = remote_svr + ":5156"
        sub_addr = remote_svr + ":5155"
        simctrl = sim.Control(pub_addr=pub_addr)

        # spawn casu and bee into the simulator
        # (type, name, coordinaets)
        # coordinates: x,y,orientation(rad)
        simctrl.spawn('Casu', 'casu-001', (0,0,0))
        simctrl.spawn('Bee', 'bee-1', (3,5,0))


