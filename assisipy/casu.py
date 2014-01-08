# The Casu API implementation

import threading
import time

import zmq

class Casu:
    """ The low-level interface to Casu devices. """
    
    def __init__(self, rtc_file_name=''):
        """ Connect to the data source. """
        
        if rtc_file_name:
            # Parse the rtc file
            pass
        else:
            # Use default values
            self.__pub_addr = 'tcp://127.0.0.1:5556'
            self.__sub_addr = 'tcp://127.0.0.1:5555'
            self.__name = 'Casu'
            self.__ir_range_readings = 8*[0]
            self.__temp_readings = 4*[0]
            self.__diagnostic_led = [0,0,0,0]
            self.__accel_freq = 4*[0]
            self.__accel_ampl = 4*[0]

            # Create the data update thread
            #self.__stop_thread = False
            self.__comm_thread = threading.Thread(target=self.__update_readings)
            self.__comm_thread.daemon = True
            self.__lock =threading.Lock()
            self.__comm_thread.start()

    def __update_readings(self):
        
        self.__context = zmq.Context(1)
        self.__sub = self.__context.socket(zmq.SUB)
        self.__sub.connect(self.__sub_addr)
        self.__sub.setsockopt(zmq.SUBSCRIBE, self.__name)
        
        while True:
            [name, dev, cmd, data] = self.__sub.recv_multipart()
            # Protect the copying operation with a lock
            # to make sure all of the data has been copied
            # before it's accessed
            with self.__lock:
                print((name,dev,cmd,data))


if __name__ == '__main__':
    
    casu = Casu()
    while True:
        print('Meanwhile, in the main thread...')
        time.sleep(1)
