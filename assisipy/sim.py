# Simulator control API

import threading
import time

import zmq

from msg import sim_msgs_pb2

class Control:
    """ Simulator control API. """

    def __init__(self, rtc_file_name=''):
        """ Bind the command publisher. """

        if rtc_file_name:
            # Parse the rtc file
            pass
        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__context = zmq.Context(1)
            self.__pub = self.__context.socket(zmq.PUB)
            self.__pub.bind(self.__pub_addr)
            
    def spawn(self, obj_type, obj_name, x, y, yaw):
        spawn_data = sim_msgs_pb2.Spawn()
        spawn_data.pose.position.x = x
        spawn_data.pose.position.y = y
        spawn_data.pose.orientation.z = yaw
        spawn_data.type = obj_type
        spawn_data.name = obj_name
        self.__pub.send_multipart(['sim', 'spawn', obj_type, 
                                   spawn_data.SerializeToString()])

    def kill(self, obj_name):
        pass

if __name__ == '__main__':

    sim_ctrl = Control()
    sim_ctrl.spawn('Casu', 'Casu', 10, 10, 0)
