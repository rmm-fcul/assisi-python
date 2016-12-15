Installation instructions
=========================

Below are instructions for installing the current version of the
Bee-arena software. Once the software is finalized, automatic installer
packages will be developed.

Currently, Ubuntu 16.04 (Xenial Xerus) 64-bit is the only officially
spported platform. Unofficial guides for some other platforms are
available :ref:`here <other-platforms-label>`.
In principle, installation on other Posix-compliant systems should also be possible,
but YMMV (Your Mileage May Vary :)

Check out the :ref:`upgrading notes <_upgrading-label>` if you are
upgrading from a previous installation.

Ubuntu 16.04 (Xenial) 64-bit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installling dependencies
------------------------

Ubuntu Xenial is the only officially supported platform for ASSISI
software. Efforts are made to make the software as portable as
possible, but we can not guarantee correct operation on other systems.

On Ubuntu Xenial, all of the required dependencies are available as
pre-build packages from official Ubuntu repositories.

Enki dependencies:

.. code-block:: console
  
    sudo apt-get install build-essential git cmake qt4-dev-tools libsdl1.2-dev
    sudo apt-get install libboost-dev libboost-program-options-dev libboost-system-dev
    sudo apt-get install libboost-python-dev

Playground dependencies:
                
.. code-block:: console
                
    sudo apt-get install libboost-filesystem-dev libboost-thread-dev
    sudo apt-get install libboost-timer-dev libprotobuf-dev protobuf-compiler
    sudo apt-get install libzmq3-dev libzmqpp-dev

Assisipy dependencies:

.. code-block:: console
                
    sudo apt-get install python-protobuf python-pip python-dev python-sphinx python-yaml
    sudo apt-get install python-zmq python-pygraphviz fabric

The next step is `Building the assisi software`_ 


Building the assisi software
----------------------------

There are three main components to install.

1. The assisi-playground simulator uses the **Enki simulation engine**, which
needs to be installed first:

.. code-block:: console

    mkdir -p ~/assisi/deps
    cd ~/assisi/deps
    
    git clone https://github.com/assisi/enki
    cd enki
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    cd ../../..
  

You should have enki and viewer folders in you ``/usr/local/include`` folder.

2. The **assisi-playground** itself:

.. code-block:: console

  git clone https://github.com/assisi/playground playground
  cd playground
  git submodule update --init
  mkdir build
  cd build
  cmake ..
  make
  export PATH=${PATH}:~/assisi/playground/build/playground
  cd ../..
  
3. The **python API**:

.. code-block:: console

  sudo pip install assisipy


The ``PATH`` export has to be done very time you open a new shell, so It's best to add it to the end of your ``~/.bashrc`` file. It's purpose is to enable the importing of the Assisi python API in Python programs.


Examples (optional)
-------------------

A variety of code examples are provided, which illustrate how to use the API to run simulations and execute code on the physical CASUs.

.. code-block:: console
    
    cd ~/assisi
    git clone https://github.com/assisi/assisipy-examples.git examples


Final structure
---------------


After completing all of the abovementioned steps, we should have the following folder structure:
  * assisi

    - playground
    - examples
    - deps

      + enki

(Note for older installation, e.g. Ubuntu 12.04, the ``assisi/deps`` directory
should also contain sub-directories for ``cppzmq`` and ``zeromq-3.2.4``).

    



Running and testing the software
--------------------------------

To test the software, you will first need to start the simulator:

.. code-block:: console

  cd ~/assisi/playground/build/playground
  ./assisi_playground &

Take note of the onscreen instructions for manipulating the camera view.

Get the examples from github

.. code-block:: console

  cd ~/assisi
  git clone https://github.com/assisi/assisipy-examples examples

Try running the some of the examples.

The wandering bee example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  cd ~/assisi/examples/wandering_bee
  ./spawn_bee_in_maze.py
  ./bee_wander.py
  

The single Casu and Bee example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the simulator is running, restart it.

.. code-block:: console

  cd ~/assisi/examples/casu_proxy_led
  ./spawn_casu_and_bee.py
  ./casu_proxy_led.py

The Bees in Casu array example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the simulator is running, restart it.

.. code-block:: console

  cd ~/assisi/examples/bees_in_casu_array
  ./spawn_bees_in_casu_array.py
  ./bees_wander.py

In a new terminal window:

.. code-block:: console

  ./casus_proxy_led.py


Setup for simulation via the deployment tool
--------------------------------------------

To execute simulations with the deployment tool requires some further installation.

The deployment tool is further described in :ref:`deployment_tools` and :ref:`deployment_examples`.

1. Create a new user account

.. code-block:: console

   sudo adduser assisi
   # enter a password; default for other details is ok

2. Set up an ssh key to access this account

.. code-block:: console

   # generate new key
   ssh-keygen -t rsa -b 4096 -C "local assisi account" -f ~/.ssh/id_rsa_localassisi
   ssh-add ~/.ssh/id_rsa_localassisi
   # <type passphrase for key>

   # check the new key is present in the keychain
   ssh-add -l

   # install key into new account
   ssh-copy-id -i ~/.ssh/id_rsa_localassisi.pub -o "PubKeyAuthentication=no" assisi@localhost 
   # <type password, hopefully for the last time!>

   # check login is possible, without typing a password.
   ssh assisi@localhost

   logout

3. Install assisi-python for this account

NOTE: the path for the assisipy package installation here (for assisi@localhost account) is slightly different to that for the normal login as described above.

.. code-block:: console

   ssh assisi@localhost
   cd ~
   git clone https://github.com/larics/assisi-python python
   cd python
   git submodule update --init
   ./compile_msgs.sh

   logout


4. On your normal login, update the ``PATH`` environment variable:

.. code-block:: console

   PATH=${PATH}:~/assisi/python/assisipy:

As per above, you can add this command in your ``.bashrc`` file

test that the deployment tools are on your path:

.. code-block:: console

   which deploy.py

   # should return something like
   /home/user/assisi/python/assisipy/deploy.py

5. Test a sample deployment.

.. code-block:: console

   cd ~/assisi/python/examples/deployment/simple
   assisi_playground &
   sim.py simple_3x3-sim.arena
   deploy.py sim_3x3_local.assisi
   # NOTE: ===> This stage should *not* ask for a password, else the toolflow will not work correctly.
   assisirun.py sim_3x3_local.assisi

(For more detail describing the example, see :ref:`deployment_examples`)












