#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Python interface to simulated bees. """

import threading
import time

import zmq

from msg import dev_msgs_pb2
from msg import base_msgs_pb2

# Device ID definitions (for convenience)

""" IR range sensors """
""" Right range sensor """
IR_SIDE_RIGHT = 0 #: Sensor at 90°
IR_RIGHT_FRONT = 1
IR_FRONT = 2
IR_LEFT_FRONT = 3
IR_SIDE_LEFT = 4

""" Light sensor """
LIGHT_SENSOR = 0

class Bee:
    """ 
    The low-level interface to Bee 'robots'. 
    This clas provides an api for programming bee behaviors.
    It creates a connection to the data source, i.e., the simulated bee.
    Waits for the bee of specified by 'name' to be spawned into the simulator.

    :param string rtc_file_name: Name of the run-time-configuration (RTC) file. This file specifies the simulation connection parameters and the name of the simulated bee object.
    :param string name: The name of the bee (if not specified in the RTC file).
    """
    
    def __init__(self, rtc_file_name='', name = 'Bee'):
        
        
        if rtc_file_name:
            # Parse the rtc file
            pass
        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__sub_addr = 'tcp://127.0.0.1:5555'
            self.__name = name
            self.__ir_range_readings = dev_msgs_pb2.RangeArray()
            self.__encoder_readings = dev_msgs_pb2.DiffDrive()
            self.__light_readings = base_msgs_pb2.ColorStamped()

            # Create the data update thread
            self.__connected = False
            self.__context = zmq.Context(1)
            self.__comm_thread = threading.Thread(target=self.__update_readings)
            self.__comm_thread.daemon = True
            self.__lock =threading.Lock()
            self.__comm_thread.start()

            # Connect the publisher socket
            self.__pub = self.__context.socket(zmq.PUB)
            self.__pub.connect(self.__pub_addr)

            # Wait for the connection
            while not self.__connected:
                pass
            print('{0} connected!'.format(self.__name))

            # Wait one more second to get all the data
            time.sleep(1)

    def __update_readings(self):
        """ 
        Get a message from Bee and update data. 
        """
        self.__sub = self.__context.socket(zmq.SUB)
        self.__sub.connect(self.__sub_addr)
        self.__sub.setsockopt(zmq.SUBSCRIBE, self.__name)
        
        while True:
            [name, dev, cmd, data] = self.__sub.recv_multipart()
            self.__connected = True
            if dev == 'ir':
                if cmd == 'ranges':
                    # Protect write with a lock
                    # to make sure all data is written before access
                    with self.__lock:
                        self.__ir_range_readings.ParseFromString(data)
                else:
                    print('Unknown command {0} for {1}'.format(cmd, self.__name))
            elif dev == 'base':
                if cmd == 'enc':
                    with self.__lock:
                        self.__encoder_readings.ParseFromString(data)
                else:
                    print('Unknown command {0} for Bee {1}'.format(cmd, self.__name))
            elif dev == 'Light':
                if cmd == 'Readings':
                    with self.__lock:
                        self.__light_readings.ParseFromString(data)
                else:
                    print('Unknown command {0} for Bee {1}'.format(cmd, self.__name))
            else:
                print('Unknown device {0} for Bee {1}'.format(dev, self.__name))


    def get_range(self, id):
        """ 
        Returns the range reading corresponding to sensor id. 
        """
        with self.__lock:
            return self.__ir_range_readings.range[id]

    def get_temp(self, id):
        """
        Returns the temperature reading of sensor id.
        """
        pass

    def get_vibration_frequency(self, id):
        """
        Returns the vibration frequency of sensor id.
        """
        pass

    def get_vibration_amplitude(self, id):
        """
        Returns the vibration amplitude of sensor id.
        """
        pass

    def get_light_rgb(self, id):
        """
        :return: (r,g,b) tuple, representing the light intensities at
                 red, green and blue wavelengths (currently, the sensor
                 reports only blue intensity, r and g are always 0).
        """
        with self.__lock:
            return (self.__light_readings.color.red,
                    self.__light_readings.color.green,
                    self.__light_readings.color.blue)

    def set_vel(self, vel_left, vel_right):
        """ 
        Set wheel velocities. 

        Bee body velocities depend on wheel velocities in the following way:
        
        .. math:: v = \\frac{v_{left}+v_{right}}{2}
        .. math:: \\omega = \\frac{v_{right}-v_{left}}{d}

        where d is the distance between the wheels ("axle length").

        :param float vel_left: Left wheel velocity.
        :param float vel_right: Right wheel velocity.
        """
        vel = dev_msgs_pb2.DiffDrive();
        vel.vel_left = vel_left
        vel.vel_right = vel_right
        self.__pub.send_multipart([self.__name, "base", "vel", 
                                   vel.SerializeToString()])

if __name__ == '__main__':
    
    bee1 = Bee(name = 'Bee')
    bee1.set_vel(5, 5)
    while True:
        for i in range(8):
            print('{0} '.format(bee1.get_range(i)))

