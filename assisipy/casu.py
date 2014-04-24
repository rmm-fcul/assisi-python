#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Python interface to CASU functionality. """

import threading
import time

import zmq

import yaml # For parsing configuration (.rtc) files

# For logging
from datetime import datetime
import csv  

from msg import dev_msgs_pb2
from msg import base_msgs_pb2

# Device ID definitions (for convenience)

""" IR range sensors """
""" Range sensor pointing to 0° (NORTH) """
IR_N = 0 
IR_NE = 1
""" Range sensor pointing to 135° (SOUTH-EAST)"""
IR_SE = 2
""" Range sensor pointing to 180° (SOUTH) """
IR_S = 3
IR_SW = 4
IR_NW = 5

""" Light actuator """
LIGHT = 0

""" Top diagnostic LED """
DLED_TOP = 0

""" Temperature sensors """
T_N = 0 #: Temperature sensor at 0°
T_E = 1
T_S = 2
T_W = 3

""" Temperature actuator """
T_ACT = 0

""" Vibration sensors """
V_N = 0
V_E = 1
V_S = 2
V_W = 3

""" Vibration actuator """
V_ACT = 0

class Casu:
    """ 
    The low-level interface to Casu devices.

    Initializes the object and starts listening for data. 
    The fully constructed object is returned only after
    the data connection has been established.

    :param string rtc_file_name: Name of the run-time configuration (RTC) file. If no file is provided, the default configuration is used.
    :param string name: Casu name (if a RTC file is provided, this value is overridden).
    :param bool log: A variable indicating whether to log all incoming and outgoing data. If set to true, a logfile in the form 'YYYY-MM-DD-HH-MM-SS-name.csv' is created.
    """
    
    def __init__(self, rtc_file_name='', name = 'Casu', log = False):
        
        if rtc_file_name:
            # Parse the rtc file
            with open(rtc_file_name) as rtc_file:
                rtc = yaml.safe_load(rtc_file)
            self.__name = rtc['name']
            self.__pub_addr = rtc['pub_addr']
            self.__sub_addr = rtc['sub_addr']
            self.__msg_pub_addr = rtc['msg_addr']
            self.__neighbors = rtc['neighbors']
        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__sub_addr = 'tcp://127.0.0.1:5555'
            self.__name = name
            self.__neighbors = None
            self.__msg_pub_addr = None
            self.__msg_sub = None

        self.__stop = False

        # TODO: Fill range_readings with fake data
        #       to prevent program crashes.
        self.__ir_range_readings = dev_msgs_pb2.RangeArray()
        self.__temp_readings = 4*[0]
        self.__diagnostic_led = [0,0,0,0]
        self.__accel_freq = 4*[0]
        self.__accel_ampl = 4*[0]

        # Create the data update thread
        self.__connected = False
        self.__context = zmq.Context(1)
        self.__comm_thread = threading.Thread(target=self.__update_readings)
        self.__comm_thread.daemon = True
        self.__lock =threading.Lock()

        # Set up logging
        self.__log = log
        if log:
            now_str = datetime.now().__str__().split('.')[0]
            now_str = now_str.replace(' ','-').replace(':','-')
            self.__logfile = open(now_str + '-' + self.__name + '.csv','wb')
            self.__logger = csv.writer(self.__logfile,delimiter=';')

        # Create inter-casu communication sockets
        self.__msg_queue = []
        if self.__msg_pub_addr:
            self.__msg_pub = self.__context.socket(zmq.PUB)
            self.__msg_pub.bind(self.__msg_pub_addr)
            self.__msg_sub = self.__context.socket(zmq.SUB)
            for direction in self.__neighbors:
                self.__msg_sub.connect(self.__neighbors[direction]['address'])
            self.__msg_sub.setsockopt(zmq.SUBSCRIBE, self.__name)
        
        # Connect the control publisher socket
        self.__pub = self.__context.socket(zmq.PUB)
        self.__pub.connect(self.__pub_addr)
        
        # Connect to the device and start receiving data
        self.__comm_thread.start()
        # Wait for the connection
        while not self.__connected:
            pass
        print('{0} connected!'.format(self.__name))
            
        # Wait one more second to get all the data
        time.sleep(0.5)

    def __update_readings(self):
        """ 
        Get data from Casu and update local data. 
        """
        self.__sub = self.__context.socket(zmq.SUB)
        self.__sub.connect(self.__sub_addr)
        self.__sub.setsockopt(zmq.SUBSCRIBE, self.__name)
        
        while not self.__stop:
            [name, dev, cmd, data] = self.__sub.recv_multipart()
            self.__connected = True
            if dev == 'IR':
                if cmd == 'Ranges':
                    # Protect write with a lock
                    # to make sure all data is written before access
                    with self.__lock:
                        self.__ir_range_readings.ParseFromString(data)
                    self.__write_to_log([time.time()] + [r for r in self.__ir_range_readings.range])
                else:
                    print('Unknown command {0} for {1}'.format(ranges, self.__name))
            else:
                print('Unknown device ir for {0}'.format(self.__name))
            
            if self.__msg_sub:
                try:
                    [name, msg, sender, data] = self.__msg_sub.recv_multipart(zmq.NOBLOCK)
                    # Protect the message queue update with a lock
                    with self.__lock:
                        self.__msg_queue.append({'sender':sender, 'data':data})
                except zmq.ZMQError:
                    # Nobody is sending us a message. No biggie.
                    pass

    def __cleanup(self):
        """
        Performs necessary cleanup operations, i.e. stops communication threads,
        closes connections and files.
        """        
        # Wait for communicaton threads to finish
        self.__comm_thread.join()

        if self.__log:
            self.__logfile.close()

    def stop(self):
        """
        Stops the Casu interface and cleans up.
        """
        self.__stop = True
        self.__cleanup()


    def get_range(self, id):
        """ 
        Returns the range reading (in cm) corresponding to sensor id. 

        .. note::
           
           This API call might become deprecated in favor of get_raw_value,
           to better reflect actual sensor capabilities.
        """
        with self.__lock:
            return self.__ir_range_readings.range[id]
        
    def get_ir_raw_value(self, id):
        """ 
        Returns the raw value from the IR proximity sensor corresponding to sensor id. 
        
        """
        with self.__lock:
            return self.__ir_range_readings.raw_value[id]

    def get_temp(self, id):
        """
        Returns the temperature reading of sensor id. 

        .. note::
           
           NOT implemented!
        """
        pass

    def set_temp(self, id, temp):
        """
        Sets the temperature reference of actuator id to temp.

        .. note::
           
           NOT implemented!

        """
        pass

    def temp_standby(self, id):
        """
        Turn the temperature actuator off.

        .. note::
           
           NOT implemented!

        """
        pass

    def set_vibration_freq(self, id, f):
        """
        Sets the vibration frequency of the pwm motor.
        
        :param float f: Vibration frequency, between 0 and 500 Hz.
        """
        
        vibration = dev_msgs_pb2.Vibration()
        vibration.freq = f
        vibration.amplitude = 0
        self.__pub.send_multipart([self.__name, "VibeMotor", "On",
                                   vibration.SerializeToString()])
        

    def get_vibration_freq(self, id):
        """
        Returns the vibration frequency of actuator id.

        .. note::

           NOT implemented!
        """
        pass

    def get_vibration_amplitude(self, id):
        """ 
        Returns the vibration amplitude of actuator id.
        """
        pass

    def vibration_standby(self, id):
        """
        Turn the vibration actuator id off.
        """
        
        vibration = dev_msgs_pb2.Vibration()
        vibration.freq = 0
        vibration.amplitude = 0
        self.__pub.send_multipart([self.__name, "VibeMotor", "Off",
                                   vibration.SerializeToString()])

    def set_light_rgb(self, id, r, g, b):
        """
        Set the color and intensity of the light actuator.
        Automatically turns the actuator on.

        :param float r: Red component intensity, between 0 and 1.
        :param float g: Green component intensity, between 0 and 1.
        :param float b: Blue component intensity, between 0 and 1.
        """
        light = base_msgs_pb2.ColorStamped()
        light.color.red = r
        light.color.green = g
        light.color.blue = b
        self.__pub.send_multipart([self.__name, "Light", "On",
                                   light.SerializeToString()])

    def light_standby(self, id):
        """
        Turn the light actuator off.
        """
        light = base_msgs_pb2.ColorStamped()
        light.color.red = 0
        light.color.green = 0
        light.color.blue = 0
        self.__pub.send_multipart([self.__name, "Light", "Off",
                                   light.SerializeToString()])

    def set_diagnostic_led_rgb(self, id, r, g, b):
        """ 
        Set the diagnostic LED light color. Automatically turns the actuator on.

        :param float r: Red component intensity, between 0 and 1.
        :param float g: Green component intensity, between 0 and 1.
        :param float b: Blue component intensity, between 0 and 1.
        """
        light = base_msgs_pb2.ColorStamped()
        light.color.red = r
        light.color.green = g
        light.color.blue = b
        self.__pub.send_multipart([self.__name, "DiagnosticLed", "On", 
                                   light.SerializeToString()])

    def get_diagnostic_led_rgb(self, id):
        """ 
        Get the diagnostic light RGB value. 

        :return: An (r,g,b) tuple (values between 0 and 1).
        """
        pass

    def diagnostic_led_standby(self, id):
        """ 
        Turn the diagnostic LED off.
        """
        light = base_msgs_pb2.ColorStamped();
        light.color.red = 0
        light.color.green = 0
        light.color.blue = 0
        self.__pub.send_multipart([self.__name, "DiagnosticLed", "Off",
                                  light.SerializeToString()])

    def send_message(self, direction, msg):
        """
        Send a simple string message to one of the neighbors.
        """
        success = False
        if direction in self.__neighbors:
            self.__msg_pub.send_multipart([self.__neighbors[direction]['name'], 'Message', 
                                           self.__name, msg])
            success = True
        
        return success

    def read_message(self):
        """
        Retrieve the latest message from the buffer.
        
        Returns a dictionary with sender(string), and data (string) fields.
        """
        msg = []
        if self.__msg_queue:
            with self.__lock:
                msg = self.__msg_queue.pop()
        
        return msg

    def __write_to_log(self, data):
        """
        Write one line of data to the logfile.
        """
        if self.__log:
            self.__logger.writerow(data)

if __name__ == '__main__':
    
    casu1 = Casu()
    switch = -1
    count = 0
    while count < 10:
        print(casu1.get_range(IR_N))
        if switch > 0:
            casu1.diagnostic_led_standby(DLED_TOP)
        else:
            casu1.set_diagnostic_led_rgb(DLED_TOP, 1, 0, 0)
        switch *= -1
        time.sleep(1)
        count = count + 1

    casu1.stop()
