Deployment instructions
=======================

Below are instructions for deploying Casu controllers to the
simulator, and to the Beaglebone boards. This manual procedure
will eventually be replaced by automatic deployment tools.

Deployment to the simulator
---------------------------

Run the simulator and start the requried applicaitons. 
Check out the examples.

Todo: Add more details about deployment of separate controller executables.

Deployment to the Casus
-----------------------

In short, you need copy the controller executables to the Casu 
controller board (BeagleBone), and run them from there. Detailed
instructions are below.

Set up the network
~~~~~~~~~~~~~~~~~~

Connect your computer to the Casu-switch by an Ethernet cable. Casus
have IPv4 adresses in the range ``192.168.12.101 - 192.168.12.104``. You
need to configure your network card with the following settings:

.. code-block:: console

      address: 192.168.12.5
      netmask: 255.255.255.0

In fact, you can use any address on the ``192.168.12.x`` subnet,
outside of the Casu range.

Add the Casu IPs and names to your ``/etc/hosts`` files (you need to
do this only once):

.. code-block:: console

      # Casus
      192.168.12.101  casu-001
      192.168.12.102  casu-002
      192.168.12.103  casu-003
      192.168.12.104  casu-004


Copy the controller executables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copy your code (.py) to the Casu to which you want to
deploy. Username/password for all Casus are ``assisi``/``assisi``.

.. code-block:: console

      scp <path to your controller file>/<your controller file>.py assisi@Casu-0x-0y:/home/assisi/controllers

If necessary, make changes to the .rtc file, e.g., change the ``name``
parameter to refer to the Casu that you are deploying to. See 
`Run-Time Configuration (.rtc) file structure`_ for details. Then,
copy the configuration file to the casu.


.. code-block:: console

      scp <path to your configuration file/Casu.rtc assisi@Casu-0x-0y:/home/assisi/controllers


Run the executables on the Casu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to the casu with two ssh consoles:

.. code-block:: console

      ssh assisi@Casu-0x-0y

In the first console, run the Casu firmware:

.. code-block:: console

   firmware/casu-fw

In the second console, run your controller:

.. code-block:: console

      chmod +x controllers <your controller name>.py
      controllers/<your controller name>.py


Run-Time Configuration (.rtc) file structure
--------------------------------------------


.. code-block:: yaml

      # Run-Time Configuration file for Casu 01-01
      # Suitable for local simulation and Casu deployment
      
      # Name of the Casu to connect to
      # Casu naming convention is casu-0xy, where xy denotes the
      # ordinal number of the casu
      name     : Casu-001
      
      # Address at which the Casu listens for incoming commands
      # (i.e., the address to which the controller publishes
      # control commands).
      # 
      # Default value (local simulator and on-Casu deployment):
      # tcp://127.0.0.1:5556
      pub_addr : tcp://127.0.0.1:5556
      
      # Address to which the Casu publishes sensor data
      # (i.e., address from which the controller
      # reads sensor data).
      #
      # Default value (local simulator and on-Casu deployment):
      # tcp://127.0.0.1:5555
      sub_addr : tcp://127.0.0.1:5555
