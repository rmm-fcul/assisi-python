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

      scp <path to your controller file>/<your controller file>.py assisi@Casu-0xy:/home/assisi/controllers

If necessary, make changes to the .rtc file, e.g., change the ``name``
parameter to refer to the Casu that you are deploying to. See 
`Run-Time Configuration (.rtc) file structure`_ for details. Then,
copy the configuration file to the casu.


.. code-block:: console

      scp <path to your configuration file/Casu.rtc assisi@Casu-0xy:/home/assisi/controllers


Run the executables on the Casu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to the casu with two ssh consoles:

.. code-block:: console

      ssh assisi@Casu-0xy

In the first console, run the Casu firmware:

.. code-block:: console

   firmware/casu-fw

In the second console, run your controller:

.. code-block:: console

      chmod +x controllers <your controller name>.py
      controllers/<your controller name>.py


.. _rtc_structure:

Run-Time Configuration (.rtc) file structure
--------------------------------------------

Rtc files tell the Python controllers the necessary details about the
Casu device they are connecting to. 

Real casu .rtc file example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/logging/casu-004.rtc
   :language: yaml

Simulated casu .rtc file example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/logging/casu-004_sim.rtc
   :language: yaml
