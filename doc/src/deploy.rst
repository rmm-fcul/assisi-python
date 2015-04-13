Deployment instructions
=======================

Below are instructions for deploying Casu controllers to the
simulator, and to the Beaglebone boards. This manual procedure
will eventually be replaced by automatic deployment tools.

Automatic deployment (command-line tools)
-----------------------------------------

.assisi
.arena
.nbg
.dep

deploy.py

assisirun.py

/HOME/.ssh/id_rsa.pub

ssh-keygen -t rsa

cat /HOME/.ssh/id_rsa.pub | ssh assisi@casu-00x 'cat >>
.ssh/authorized_keys'

http://www.linuxproblem.org/art_9.html


Deployment to the simulator
---------------------------

Run the simulator and start the requried applicaitons. 
Check out the examples.

Todo: Add more details about deployment of separate controller executables.

Manual deployment to the Casus
------------------------------

You have two options for controlling the Casus. The simpler option is
**Remote deployment**, which implies running the controller on the
*master workstation*. **Local** or **On-casu deployment** requires
copying your code to the Casu board (Beaglebone) and running it from
there. Either way, your network needs to be set up correctly. 

Set up the network
~~~~~~~~~~~~~~~~~~

Connect your computer (this is what we call the * master workstation*
to the Casu-switch by an Ethernet cable). Casus have IPv4 adresses in
the range ``192.168.12.101 - 192.168.12.104``. You need to configure
your network card with the following settings: 

.. code-block:: console

      address: 192.168.12.x
      netmask: 255.255.255.0

Where x can be any number outside of the Casus' range.

Add the Casu IPs and names to your ``/etc/hosts`` files (you need to
do this only once):

.. code-block:: console

      # Casus
      192.168.12.101  casu-001
      192.168.12.102  casu-002
      192.168.12.103  casu-003
      192.168.12.104  casu-004

Remote deployment
~~~~~~~~~~~~~~~~~

For remote deployment, you need check two things:

   #. you have the appropriate .rtc file (check out the `Run-Time Configuration (.rtc) file structure`_ for details)
   #. you are connected to the Casu network and the Casu you want to control is powered; Check this by pinging the Casu:

.. code-block:: console

   ping casu-001

**Note:** The Casu firmware is started automatically after booting the
Beaglebone, but the startup might take up to two minutes, so be
patient :)

Local (on-Casu) deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~

In short, you need copy the controller executables to the Casu 
controller board (BeagleBone), and run them from there. 

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

Now you are ready to run the executables on the Casu.

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
