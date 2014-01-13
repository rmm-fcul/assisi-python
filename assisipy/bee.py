# The Casu API implementation

import threading
import time

import zmq

from msg import dev_msgs_pb2
from msg import base_msgs_pb2

# Device ID definitions (for convenience)

# IR range sensors
IR_SIDE_RIGHT = 0
IR_RIGHT_FRONT = 1
IR_FRONT = 2
IR_LEFT_FRONT = 3
IR_SIDE_LEFT = 4

class Bee:
    """ The low-level interface to Bee 'robots'. """
    
    def __init__(self, rtc_file_name='', name = 'Bee'):
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
            self.__encoder_readings = dev_msgs_pb2.DiffDrive()

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
        """ Get message from Bee and update data. """
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
                    print('Unknown command {0} for {1}'.format(cmd, self.__name))
            else:
                print('Unknown device ir for {0}'.format(self.__name))


    def get_range(self, id):
        """ Returns the range reading corresponding to sensor id. """
        with self.__lock:
            return self.__ir_range_readings.range[id]

    def set_vel(self, vel_left, vel_right):
        """ Set wheel velocities."""
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

