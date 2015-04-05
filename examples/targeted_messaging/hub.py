#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Control of the central Casu
# This responds to different incoming messages, in a different manner
# according to the label.

from assisipy import casu
import argparse, os
import time

import yaml
def find_comm_links(rtc, verb=False):
    phys_logi_map = {}

    try:
        deploy = yaml.safe_load(file(rtc, 'r'))
        # verify that the deployment file is for the same named object
        if 'neighbors' in deploy and deploy['neighbors'] is not None:
            for k, v in deploy['neighbors'].iteritems():
                neigh = v.get('name', None)
                if verb: print v, neigh
                if neigh:
                    phys_logi_map[neigh] = k

    except IOError:
        print "[W] could not read rtc conf file for casu {}".format(casu_name)
    
    return phys_logi_map




class CasuController(object):

    def __init__(self, rtc_file, verb=True):
        self.__casu = casu.Casu(rtc_file)
        self.old_state = 'Off'
        self.state = 'Off'
        self.verb = verb
        self._comm_links = find_comm_links(rtc_file, verb=self.verb)

    def stop(self):
        self.__casu.stop()

    def react_to_neighbors(self):
        '''
        read messages from afar, and change color according to the *channel* 
        that the incoming message came from.  (optionally, message payload
        indicates different factor - like how long to flash for/how intense?)

        '''

        msgs = self.recv_all_msgs(retry_cnt=0, max_recv=None)
        for msg in msgs:
            src_physical = msg['sender']
            src_label = self._comm_links.get(src_physical, None)

            if src_label in ['red', 'green']:
                self.old_state = self.state
                self.state = "{} {}".format(src_label, msg['data'])
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'

            if self.verb:
                print "[I] rx msg from {} (link {}), new state is {}".format(
                        src_physical, src_label, self.state)

        if self.old_state != self.state:
            if self.state == 'red On':
                self.__casu.set_diagnostic_led_rgb(1, 0, 0, casu.DLED_TOP)
            elif self.state == 'green On':
                self.__casu.set_diagnostic_led_rgb(0, 1, 0, casu.DLED_TOP)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)




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
                    print "\t[i]<== recv msg ({1} by): from {0}".format(
                        msg['sender'], len(msg['data']) )
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



    def react_to_bees(self):
        """
        Changes color to red, when a bee is detected by one of the proximity sensors.
        Notifies neighbor.
        """
        while True:
            if self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
                self.old_state = self.state
                self.state = 'Red On'
            elif (self.__casu.get_range(casu.IR_NE) < 2 or
                  self.__casu.get_range(casu.IR_SE) < 2):
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 1, 0)
                self.old_state = self.state
                self.state = 'Green On'
            elif self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 0, 1)
                self.old_state = self.state
                self.state = 'Blue On'
            elif (self.__casu.get_range(casu.IR_SW) < 2 or
                  self.__casu.get_range(casu.IR_NW) < 2):
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 1, 0)
                self.old_state = self.state
                self.state = 'Yellow On'
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'

            if self.old_state != self.state:
                if self.old_state == 'Red On':
                    self.__casu.send_message('north', 'Off')
                elif self.old_state == 'Green On':
                    self.__casu.send_message('east', 'Off')
                elif self.old_state == 'Blue On':
                    self.__casu.send_message('south', 'Off')
                elif self.old_state == 'Yellow On':
                    self.__casu.send_message('west', 'Off')

                if self.state == 'Red On':
                    self.__casu.send_message('north', 'On')
                if self.state == 'Green On':
                    self.__casu.send_message('east', 'On')
                if self.state == 'Blue On':
                    self.__casu.send_message('south', 'On')
                if self.state == 'Yellow On':
                    self.__casu.send_message('west', 'On')



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

    ctrl = CasuController(rtc_file=rtc)

    try:
        while True:
            ctrl.react_to_neighbors()
            #time.sleep(0.5)
    except KeyboardInterrupt:
        # cleanup
        ctrl.stop()



        
        

