#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Control of the central Casu

This responds to different incoming messages, in a different manner
according to the label / "channel name" (which is independent from
the physical name of the sender)
'''

from assisipy import casu
import argparse, os
#import time


class CasuController(object):

    def __init__(self, rtc_file, verb=True):
        self.__casu = casu.Casu(rtc_file)
        self.old_state = 'Off'
        self.state = 'Off'
        self.rgb  = [0,0,0]
        self.verb = verb
        #self._comm_links = find_comm_links(rtc_file, verb=self.verb)

    def stop(self):
        self.rgb  = [0,0,0]
        self.__casu.set_diagnostic_led_rgb(*self.rgb)#, casu.DLED_TOP)
        self.__casu.stop()

    def react_to_neighbors(self):
        '''
        read messages from afar, and change color according to the *channel*
        that the incoming message came from.  (optional extension, message
        payload indicates different factor - like how long to flash for/how
        intense?)

        '''

        msgs = self.recv_all_msgs(retry_cnt=0, max_recv=None)
        for msg in msgs:
            src_physical = msg['sender']
            #src_label = self._comm_links.get(src_physical, None)
            src_label = msg['label']

            if src_label in ['red', 'green']:
                self.old_state = self.state
                self.state = "{} {}".format(src_label, msg['data'])
                intensity = 0.0
                if msg['data'].lower() == 'on': intensity = 0.8

                if src_label == 'red':   self.rgb[0] = intensity
                if src_label == 'green': self.rgb[1] = intensity
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'
                self.rgb  = [0,0,0]
                #self.__casu.set_diagnostic_led_rgb(*self.rgb, casu.DLED_TOP)

            if self.verb:
                print "[I] rx msg from '{}' (link '{}'), new state: {}".format(
                        src_physical, src_label, self.state)

        if self.old_state != self.state:
            self.__casu.set_diagnostic_led_rgb(*self.rgb)# casu.DLED_TOP)
            #if self.state == 'red On':
            #    self.__casu.set_diagnostic_led_rgb(1, 0, 0, casu.DLED_TOP)
            #elif self.state == 'green On':
            #    self.__casu.set_diagnostic_led_rgb(0, 1, 0, casu.DLED_TOP)
            #else:
            #    self.__casu.diagnostic_led_standby(casu.DLED_TOP)



    def recv_all_msgs(self, retry_cnt=0, max_recv=None):
        '''
        continue to read message bffer until no more messages.
        return as list of messages (each msg is a dict)

        '''
        msgs = []
        try_cnt = 0

        while(True):
            msg = self.__casu.read_message()
            #print msg
            if msg:
                msgs.append(msg)

                if self.verb:
                    print "\t[i]<== recv msg ({1} by): from {0} ('{2}')".format(
                        msg['sender'], len(msg['data']), msg['label'] )
                if self.verb > 1:
                    print msg.items()

                if(max_recv is not None and len(msgs) >= max_recv):
                    break
            else:
                # buffer emptied, return
                try_cnt += 1
                if try_cnt > retry_cnt:
                    break

        return msgs



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--rtc-path', type=str, default='',
            help="location of RTC files to configure CASUs",)
    parser.add_argument('-n', '--name', type=str, default='casu-ctr',
            help="location of RTC files to configure CASUs",)
    parser.add_argument('-v', '--verb', type=int, default=1,
            help="verbosity level")
    args = parser.parse_args()

    fname = "{}.rtc".format(args.name)
    rtc = os.path.join(args.rtc_path, fname)
    print "connecting to casu {} ('{}')".format(args.name, rtc)

    ctrl = CasuController(rtc_file=rtc, verb=args.verb)

    try:
        while True:
            ctrl.react_to_neighbors()
    except KeyboardInterrupt:
        # cleanup
        ctrl.stop()



