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
LIGHT_ACT = 6

""" Top diagnostic LED """
DLED_TOP = 7

""" Temperature sensors """
TEMP_N = 8 #: Temperature sensor at 0°
TEMP_E = 9
TEMP_S = 10
TEMP_W = 11
TEMP_TOP = 12

""" Temperature actuator """
PELTIER_ACT = 13

""" Vibration sensors """
VIBE_N = 14
VIBE_E = 15
VIBE_S = 16
VIBE_W = 17

""" Vibration actuator """
VIBE_ACT = 18

""" E-M actuator """
EM_ACT = 19

""" E-M actuator modes """
EM_MODE_ELECTRIC = 0
EM_MODE_MAGNETIC = 1
EM_MODE_HEAT = 2


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
            self.__msg_sub = None

        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__sub_addr = 'tcp://127.0.0.1:5555'
            self.__name = name
            self.__neighbors = None
            self.__msg_pub_addr = None
            self.__msg_sub = None

        self.__stop = False

        # TODO: Fill readings with fake data
        #       to prevent program crashes.
        self.__ir_range_readings = dev_msgs_pb2.RangeArray()
        self.__temp_readings = dev_msgs_pb2.TemperatureArray()
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
                    self.__write_to_log(['ir', time.time()] + [r for r in self.__ir_range_readings.range])
                else:
                    print('Unknown command {0} for {1}'.format(cmd, self.__name))
            elif dev == 'Temp':
                if cmd == 'Temperatures':
                    with self.__lock:
                        self.__temp_readings.ParseFromString(data)
                    self.__write_to_log(['temp', time.time()] + [t for t in self.__temp_readings.temp])
                else:
                    print('Unknown command {0} for {1}'.format(cmd, self.__name))
            else:
                print('Unknown device {0} for {1}'.format(dev, self.__name))
            
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

        TODO: Need to disable all operations once Casu is stopped!
        """
        self.__stop = True
        self.__cleanup()
        print('{0} disconnected!'.format(self.__name))


    def config_em(self, id = EM_ACT, mode = EM_MODE_ELECTRIC):
        """
        Configure the EM device mode.
        """
        config = dev_msgs_pb2.EMDeviceConfig()
        if mode == EM_MODE_ELECTRIC:
            config.mode = dev_msgs_pb2.EMDeviceConfig.ELECTRIC
        elif mode == EM_MODE_MAGNETIC:
            config.mode = dev_msgs_pb2.EMDeviceConfig.MAGNETIC
        elif mode == EM_MODE_HEAT:
            config.mode = dev_msgs_pb2.EMDeviceConfig.HEAT
        self.__pub.send_multipart([self.__name, "EM", "config",
                                   config.SerializeToString()])
        self.__write_to_log(["em_config", time.time(), mode])

    def get_range(self, id):
        """ 
        Returns the range reading (in cm) corresponding to sensor id. 

        .. note::
           
           This API call might become deprecated in favor of get_raw_value,
           to better reflect actual sensor capabilities.
        """
        with self.__lock:
            if self.__ir_range_readings.range:
                return self.__ir_range_readings.range[id]
            else:
                return -1
        
    def get_ir_raw_value(self, id):
        """ 
        Returns the raw value from the IR proximity sensor corresponding to sensor id. 
        
        """
        with self.__lock:
            if self.__ir_range_readings.raw_value:
                return self.__ir_range_readings.raw_value[id]
            else:
                return -1

    def get_temp(self, id):
        """
        Returns the temperature reading of sensor id. 

         """
        with self.__lock:
            if self.__temp_readings.temp:
                return self.__temp_readings.temp[id - TEMP_N]
            else:
                return -1

    def set_temp(self, id = PELTIER_ACT, temp = 36):
        """
        Sets the temperature reference of actuator id to temp.

        """
        temp_msg = dev_msgs_pb2.Temperature()
        temp_msg.temp = temp
        device = "peltier"
        if id == EM_ACT:
            device = "EM"
        self.__pub.send_multipart([self.__name, device, "temp",
                                   temp_msg.SerializeToString()])
        self.__write_to_log([device + "_temp", time.time(), temp])

    def temp_standby(self, id = PELTIER_ACT):
        """
        Turn the temperature actuator off.

        """
        temp_msg = dev_msgs_pb2.Temperature()
        temp_msg.temp = 0
        device = "peltier"
        if id == EM_ACT:
            device = "EM"
        self.__pub.send_multipart([self.__name, device, "Off",
                                   temp_msg.SerializeToString()])
        self.__write_to_log([device + "_temp", time.time(), 0])

    def set_vibration_freq(self, id = VIBE_ACT, f = 0):
        """
        Sets the vibration frequency of the pwm motor.
        
        :param float f: Vibration frequency, between 0 and 500 Hz.
        """
        
        vibration = dev_msgs_pb2.Vibration()
        vibration.freq = f
        vibration.amplitude = 0
        self.__pub.send_multipart([self.__name, "VibeMotor", "On",
                                   vibration.SerializeToString()])
        self.__write_to_log(["vibe_ref", time.time(), f])

    def get_vibration_freq(self, id = VIBE_ACT):
        """
        Returns the vibration frequency of actuator id.

        .. note::

           NOT implemented!
        """
        pass

    def get_vibration_amplitude(self, id = VIBE_ACT):
        """ 
        Returns the vibration amplitude of actuator id.
        """
        pass

    def vibration_standby(self, id  = VIBE_ACT):
        """
        Turn the vibration actuator id off.
        """
        
        vibration = dev_msgs_pb2.Vibration()
        vibration.freq = 0
        vibration.amplitude = 0
        self.__pub.send_multipart([self.__name, "VibeMotor", "Off",
                                   vibration.SerializeToString()])
        self.__write_to_log(["vibe_ref", time.time(), 0])

    def set_light_rgb(self, id = LIGHT_ACT, r = 0, g = 0, b = 0):
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
        self.__write_to_log(["light_ref", time.time(), r, g, b])

    def light_standby(self, id = LIGHT_ACT):
        """
        Turn the light actuator off.
        """
        light = base_msgs_pb2.ColorStamped()
        light.color.red = 0
        light.color.green = 0
        light.color.blue = 0
        self.__pub.send_multipart([self.__name, "Light", "Off",
                                   light.SerializeToString()])
        self.__write_to_log(["light_ref", time.time(), 0, 0, 0])

    def set_diagnostic_led_rgb(self, id = DLED_TOP, r = 0, g = 0, b = 0):
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
        self.__write_to_log(["dled_ref", time.time(), r, g, b])

    def get_diagnostic_led_rgb(self, id = DLED_TOP):
        """ 
        Get the diagnostic light RGB value. 

        :return: An (r,g,b) tuple (values between 0 and 1).
        """
        pass

    def diagnostic_led_standby(self, id = DLED_TOP):
        """ 
        Turn the diagnostic LED off.
        """
        light = base_msgs_pb2.ColorStamped();
        light.color.red = 0
        light.color.green = 0
        light.color.blue = 0
        self.__pub.send_multipart([self.__name, "DiagnosticLed", "Off",
                                  light.SerializeToString()])
        self.__write_to_log(["dled_ref", time.time(), 0, 0, 0])

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
