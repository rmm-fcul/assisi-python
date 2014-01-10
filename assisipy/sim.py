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
            self.__pub.connect(self.__pub_addr)
            
    def spawn(self, 
              obj_type, 
              name, 
              pose, 
              polygon = (), 
              radius = (), 
              color = (),
              height = 1,
              mass = -1):
        """ Spawn an object in the simulated world.
            
            Parameters
            ----------
            obj_type : Type of object to spawn. Currently supported types are
                       'Casu', 'EPuck' and 'Physical'
            name : Name of the object. Must be unique in the world.
            pose : An (x,y,yaw) tuple.
            polygon : A tuple of vertex coordinates ((x1,y1),(x2,y2),...).
                      If obj_type is 'Physical', this defines the shape of the
                      object.
            radius : Radius of a cylindrical 'Physical' object. 
            color : Color of a 'Physical' object.
            height : 'Physical' object height.
            mass : 'Physical' object mass.

            Returns
            -------
            Nothing
        """
        data = sim_msgs_pb2.Spawn()
        data.pose.position.x = pose[0]
        data.pose.position.y = pose[1]
        data.pose.orientation.z = pose[2]
        data.type = obj_type
        data.name = name
        if len(color) == 3:
            data.color.red = color[0]
            data.color.green = color[1]
            data.color.blue = color[2]
        if (obj_type == 'Physical') and radius:
            data.cylinder.radius = radius
            data.cylinder.height = height
            data.cylinder.mass = mass
            data.type = 'Cylinder'
        if (obj_type == 'Physical') and polygon:
            for vertex in polygon:
                v = data.polygon.vertices.add()
                v.x = vertex[0]
                v.y = vertex[1]
            data.polygon.height = height
            data.polygon.mass = mass
            data.type = 'Polygon'
        self.__pub.send_multipart(['sim', 'spawn', obj_type, 
                                   data.SerializeToString()])

    def kill(self, obj_name):
        pass

if __name__ == '__main__':

    sim_ctrl = Control()
    sim_ctrl.spawn('Casu', 'Casu', 10, 10, 0)