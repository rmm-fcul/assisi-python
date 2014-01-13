# The Casu API implementation

import threading
import time

import zmq

from msg import dev_msgs_pb2
from msg import base_msgs_pb2

# Device ID definitions (for convenience)

# IR range sensors
IR_N = 0
IR_NE = 1
IR_SE = 2
IR_S = 3
IR_SW = 4
IR_NW = 5

# Diagnostic LEDs
DLED_TOP = 0

class Casu:
    """ The low-level interface to Casu devices. """
    
    def __init__(self, rtc_file_name='', name = 'Casu'):
        """ Connect to the data source. """
        
        if rtc_file_name:
            # Parse the rtc file
            pass
        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__sub_addr = 'tcp://127.0.0.1:5555'
            self.__name = name
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
            self.__comm_thread.start()

            # Bind the publisher socket
            self.__pub = self.__context.socket(zmq.PUB)
            self.__pub.connect(self.__pub_addr)

            # Wait for the connection
            while not self.__connected:
                pass
            print('{0} connected!'.format(self.__name))

            # Wait one more second to get all the data
            time.sleep(1)

    def __update_readings(self):
        """ Get message from Casu and update data. """
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
                    print('Unknown command {0} for {1}'.format(ranges, self.__name))
            else:
                print('Unknown device ir for {0}'.format(self.__name))

    def get_range(self, id):
        """ Returns the range reading corresponding to sensor id. """
        with self.__lock:
            return self.__ir_range_readings.range[id]

    def set_diagnostic_led_rgb(self, id, r, g, b):
        """ Set the diagnostic LED light color. """
        light = base_msgs_pb2.ColorStamped();
        light.color.red = r
        light.color.green = g
        light.color.blue = b
        self.__pub.send_multipart([self.__name, "DiagnosticLed", "On", 
                                   light.SerializeToString()])

    def get_diagnostic_led_rgb(self, id):
        """ Get the diagnostic light rgb value. 

            returns an (r,g,b) tuple
        """
        pass

    def diagnostic_led_standby(self, id):
        """ Turn the diagnostic LED off.
        """
        light = base_msgs_pb2.ColorStamped();
        light.color.red = 0
        light.color.green = 0
        light.color.blue = 0
        self.__pub.send_multipart([self.__name, "DiagnosticLed", "Off",
                                  light.SerializeToString()])

if __name__ == '__main__':
    
    casu1 = Casu()
    switch = -1
    while True:
        print(casu1.get_range(IR_N))
        if switch > 0:
            casu1.diagnostic_led_standby(DLED_TOP)
        else:
            casu1.set_diagnostic_led_rgb(DLED_TOP, 1, 0, 0)
        switch *= -1
        time.sleep(1)
