Installation instructions
=========================

Below are instructions for installing the current version of the
Bee-arena software. Once the software is finalized, automatic installer
packages will be developed.

For maximum portability, it is also possible to install the simulator
in a virtual machine. Two minimalistic virtual machines are available:

`AssisiBeeCasuSim.ova
<http://larics.rasip.fer.hr/laricscloud/public.php?service=files&t=f909f86cc3cd2c81867120c66d687679>`_
(better image)

`ASSISIsim.ova
<http://larics.rasip.fer.hr/laricscloud/public.php?service=files&t=e8b1ac9041ee2faa52c3ce1cdd3228d9>`_
(smaller image)

The username/password for both machines are
``assisi``/``assisi``. Just start the VM, log on, and follow the
instructions, below.

**Note:** The use of a VM is completely optional. If you are running
an Ubuntu 12.04, or some other compatible system, (e.g. a newer Ubuntu
version or Debian), a native install is the way to go.

Installling dependencies
------------------------

The installation procedure has been tested on the systems listed
below, and is known to work on those systems. In principle,
installation on other Posix-compliant systems should also be possible,
but YMMV (Your Mileage May Vary :)

Ubuntu 12.04 (Precise) 64-bit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the dependencies needed to build and run ASSISI software can
be installed from official Ubuntu repositories:

.. code-block:: console
  
    sudo apt-get install build-essential git cmake qt4-dev-tools
    sudo apt-get install libboost-dev libboost-program-options-dev
    sudo apt-get install libprotobuf-dev protobuf-compiler python-protobuf
    sudo apt-get install python-dev python-zmq python-sphinx python-yaml

A few dependencies have to be installed manually. Create a folder for the Assisi project and position yourself there

.. code-block:: console
    
    cd ~
    mkdir assisi
    cd assisi

Build and install the ZeroMQ networking library:

.. code-block:: console

   mkdir deps
   cd deps
   wget http://download.zeromq.org/zeromq-3.2.4.tar.gz
   tar xvf zeromq-3.2.4.tar.gz
   cd zeromq-3.2.4
   ./configure
   make
   sudo make install
   cd ..

After this step you should have the files ``zmq.h`` and ``zmq_utils.h`` in your ``/usr/local/include`` folder.

Add ZeroMQ c++ bindings:

.. code-block:: console

    git clone https://github.com/zeromq/cppzmq
    sudo cp cppzmq/zmq.hpp /usr/local/include

Ubuntu 14.04 (Trusty) 64-bit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Ubuntu Trusty, all of the required dependencies are available as
pre-build packages from official Ubuntu repositories:

.. code-block:: console
  
    sudo apt-get install build-essential git cmake qt4-dev-tools
    sudo apt-get install libboost-dev libboost-program-options-dev
    sudo apt-get install libprotobuf-dev protobuf-compiler python-protobuf
    sudo apt-get install python-dev python-sphinx python-yaml
    sudo apt-get install libzmq3-dev python-zmq

MacOS X
~~~~~~~

TODO

Building the assisi software
----------------------------

The assisi-playground simulator uses the Enki simulation engine, which
needs to be installed first:

.. code-block:: console
    
    git clone https://github.com/larics/enki
    cd enki
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    cd ../../..
  

You should have enki and viewer folders in you ``/user/local/include`` folder.

The assisi-playground itself:

.. code-block:: console

  git clone https://github.com/larics/assisi-playground playground
  cd playground
  git submodule update --init
  mkdir build
  cd build
  cmake ..
  make
  cd ../..
  
The Pyton API

.. code-block:: console

  git clone https://github.com/larics/assisi-python python
  cd python
  git submodule update --init
  ./compile_msgs.sh
  export PYTHONPATH=${PYTHONPATH}:~/assisi/python
  cd ..

The ``PYTHONPATH`` export has to be done very time you open a new shell, so It's best to add it to the end of your ``~/.bashrc`` file. It's purpose is to enable the importing of the Assisi python API in Python programs.

After completing all of the abovementioned steps, we should have the following folder structure:
  * assisi

    - playground
    - python
    - deps

      + zeromq-3.2.4
      + cppzmq
      + enki
    
Running and testing the software
--------------------------------

To test the software, you will first need to start the simulator:

.. code-block:: console

  cd ~/assisi/playground/build/playground
  ./assisi_playground &

Take note of the onscreen instructions for manipulating the camera view.

Try running the demos in the ``python/examples`` folder.

The wandering bee example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  cd ~/assisi/python/examples/wandering_bee
  ./spawn_bee_in_maze.py
  ./bee_wander.py
  

The single Casu and Bee example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the simulator is running, restart it.

.. code-block:: console

  cd ~/assisi/python/examples/casu_proxy_led
  ./spawn_casu_and_bee.py
  ./casu_proxy_led.py

The Bees in Casu array example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the simulator is running, restart it.

.. code-block:: console

  cd ~/assisi/python/examples/bees_in_casu_array
  ./spawn_bees_in_casu_array.py
  ./bees_wander.py

In a new terminal window:

.. code-block:: console

  ./casus_proxy_led.py
