Deployment instructions
=======================

Below are instructions for deploying Casu controllers to the
simulator, and to the Beaglebone boards. Automatic deployment is the
recommended approach for "production" use (performing experiments with
larger numbers of CASUs). Manual deployment is useful when testing
things with a single Casu.

Several computers are usually involved in a deployment scenario, and
will be referred to by the following naming conventions:

* **Development host:** The computer where the user is writing
  controller code
* **Deployment target:** The computer where the controller code will
  run; If the development host and deployment target are the same, we
  are talking about **local deployment**, otherwise it's a **remote
  deployment**; it is also possible to locally deploy code which
  controlls a remote target (e.g. code is running on the development
  host, but controlling a real CASU)
* **Simulator host**: The machine where the simulator is running; Usually, this
  will be the development host, but it can also be another machine
  (e.g. in multi-simulator setups)

Network setup
-------------

This section describes the network setup necessary for deploying code
to CASUs. Generally, this procedure has to be performed only once for
a particular development host, and has already been done for the CASU Master
Workstation at the Artificial Life Lab in Graz.

Depending on your deployment scenario, only some subsections of this
document might be relevant, as outlined in the table below.

.. csv-table:: Subsection relevance for particular deployment scenarios
   :header: "Deployment target", "Deployment mode", "CASU HW/Simulation", "Relevant subsections"
   :widths: 30, 30, 30, 30
   
    "Local machine", "Automatic", "Simulation", "Paswordless ssh login"
    "Remote machine", "Automatic", "CASU HW", "All"
    "Local machine", "Manual", "Simulation", "-"
    "Local machine", "Manual", "CASU HW", "Hostname definitions"
    "Remote machine (CASU)", "Manual", "CASU HW", "Hostname definitions"


Hostname definitions
~~~~~~~~~~~~~~~~~~~~

To enable correct code deployment and execution, all the involved
machines have to be able to to resolve each other's
hostnames. Currently, this is acheived by manually editing the
``/etc/hosts`` system configuration file (requires ``sudo`` privileges). [#fdhcp]_

For local deployment and simulation, it usually suffices that
``localhost`` is defined. For remote deployment, and in the case when
code is deployed locally, but controls remote devices (real or
simulated), appropriate ``/etc/hosts`` entires are necessary. All
CASUs are connected to a local TCP/IP network with IP adresses on the
192.168.12.xxx subnet. Casu adresses start at 101, the adress space
below is reserved for development hosts. The relevant section of
``/etc/hosts`` from the Master Workstation are given below:[#fmultip]_
::

   # Casus
   192.168.12.1   control-workstation
   192.168.12.101 casu-001
   192.168.12.101 casu-002
   192.168.12.102 casu-003
   192.168.12.103 casu-004
   192.168.12.103 casu-005
   192.168.12.102 casu-006
   192.168.12.104 casu-007
   192.168.12.104 casu-008
   192.168.12.105 casu-009

.. _ssh_nopass:

.. note:: If you experience a sluggish ssh/scp connection, when connecting to
   physical CASUs:

   - Edit ``/etc/hosts`` on each of the CASU beaglebone computers, to include
     your host IP and machine name.  (i.e. beaglebone->your PC, the reverse 
     direction to above)
   - This is already set up for the CASU Master Workstation at the Artificial
     Life Lab in Graz (192.168.12.1).


Paswordless ssh login
~~~~~~~~~~~~~~~~~~~~~

Paswordless ssh login is necessary for automated deployment. It can
also save you some typing when doing manual deployment. To set it up,
you will need an ``id_rsa.pub`` key file in your ``~/.ssh``
folder. If it's not there, create it with the command:
::

   ssh-keygen -t rsa

(you can skip creating a password for your key file by just pressing
enter when prompted)

Assuming that you will be deploying your code to a machine called
``target``, you have to add your key file to the list of authorized
keys on the target machine:
::

   ssh-copy-id -i ~/.ssh/id_rsa.pub assisi@casu-0xy

Check that everything is working by logging in from the development host:
::

   ssh username@target

You should be logged in automatically, without being prompted for a
password.

If you get an error saying something similar to:
::

   Agent admitted failure to sign using the key.

just do:
::

   ssh-add

on the develpment host.

For more information check out `this howto
<http://www.linuxproblem.org/art_9.html>`_ or `this tutorial
<https://www.debian-administration.org/article/152/Password-less_logins_with_OpenSSH>`_
for a more in-depth expalanation.

This procedure is also necessary for doing automated deployment on a
local machine (i.e. the development host and deployment target are the
same machine).

Automatic deployment (GUI tool)
-------------------------------

TODO

.. _deployment_tools:

Automatic deployment (command-line tools)
-----------------------------------------

To see complete examples, as well as examine the structure and
content of deployment files, please refer to
the :ref:`deployment_examples` section. The rest of this section
provides a quick overview of the deployment process.

Automatic deployment generally consists of two steps:

#. The **deployment step**, where controllers are copied from the
   development host to the deployment target
#. The **run step**, where the deployed controller code is executed to
   control the behavior of CASUs (real or simulated)

In order to successfully perform the steps above, the user has to
prepare four files describing the details of the deployment he/she
wishes to perform:

* An **arena description file** recognized by the ``.arena``
  extension and written in `yaml <http://yaml.org/>`_ syntax, which describes 
  the physical arena layout (absolute CASU positions) 
  and CASU URIs for establishing ZeroMQ connections
* A **neighborhood file**, recognized by the ``.nbg`` extension
  and written in `Graphviz dot syntax
  <http://www.graphviz.org/content/dot-language>`_ syntax,
  which describes the inter-CASU data connection topology
* A **deployment file**, recognized by the ``.dep`` extension and
  written in `yaml <http://yaml.org/>`_ syntax, which describes 
  the desired deployment strategy, i.e., for each CASU it specifies
  the controller to be deployed and the connection details of the
  deployment target
* A **project** file, recognized by the ``.assisi`` extension, which
  lists the arena, neighborhood and deployment files that make up the
  current project

To deploy the code, simply invoke:
::

   deploy.py PROJECTFILE.assisi

After successfully running the deployment script, you will
see a local ``PROJECTFILE_sandbox`` folder containing a subfolder
layout corresponding to the ``.dep`` file specification. Each leaf
subfolder will contain the appropriate controller script and a
corresponding automatically generated ``.rtc`` file. Furthermore, the
deployment script will create a ``PROJECTFILE.py`` file, which is a `Fabric
fabfile <http://www.fabfile.org/>`_ used for running the deployed
controllers.

To run the controllers, invoke:
::

   assisirun.py PROJECTFILE.assisi

You will be able to observe program output from each of your CASU
controllers in the terminal. To stop the execution of all controllers
simultaneously, just interrupt the `assisirun.py` script by pressing
`Ctrl-C`.

If the console is garbled after terminating the `assisirun.py`
process, just type `reset` at the prompt (don't worry if you don't see
the characters as you type them), and press Enter. This will return
the console to an usable state.

To retreive the data logged by the casu controllers, run:
::

   collect_data.py sim_3x3_local.assisi --clean

The logfiles will be stored in a new subfolder called
`data_sim_3x3_local`. The `--clean` option removes the original log
files after copying them.


Other deployment options
------------------------

Remote simulator and multi-simulator setups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the simulator and start the requried applicaitons. 
Check out the examples.

Todo: Add more details about deployment of separate controller executables.

Manual deployment to the development host with simulated CASUs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the simplest option, for trying things out...

Manual deployment to the development host with real CASU hardware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have two options for controlling the Casus. The simpler option is
**Remote deployment**, which implies running the controller on the
*master workstation*. **Local** or **On-casu deployment** requires
copying your code to the Casu board (Beaglebone) and running it from
there. Either way, your network needs to be set up correctly. 

For remote deployment, you need check two things:

#. you have the appropriate .rtc file (check out the `Run-Time Configuration (.rtc) file structure`_ for details)
#. you are connected to the Casu network and the Casu you want to control is powered; Check this by pinging the Casu:

.. code-block:: console

   ping casu-001

**Note:** The Casu firmware is started automatically after booting the
Beaglebone, but the startup might take up to two minutes, so be
patient :)

Manual deployment to the CASU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

      scp <path to your configuration file/Casu.rtc assisi@casu-0xy:/home/assisi/controllers

Now you are ready to run the executables on the Casu.

Connect to the casu with two ssh consoles:

.. code-block:: console

      ssh assisi@casu-0xy

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


.. rubric:: Footnotes

.. [#fdhcp] TODO: Implement a local DHCP server.

.. [#fmultip] In the current setup, two CASU devices are connected to
             the same Beaglebone board
