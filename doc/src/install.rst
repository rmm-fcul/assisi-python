Installation instructions
=========================

Below are instructions for installing the current version of the
Bee-arena software. Once the softwer is finalized, automatic installer
packages will be developed.

A VirtualBox .ova image which has everything already set up is
available at 

http://larics.rasip.fer.hr/laricscloud/public.php?service=files&t=a55a3a1d7cfef34511e6a22a8c0387d3. 

Username/password are ``assisi``/``assisi``.

System setup
------------

The software is known to work on Ubuntu 12.04 (Precise) 64-bit. It has not been tested on other systems.

Install the tools needed to build the software:

.. code-block:: console
  
    sudo apt-get install build-essential git cmake qt4-dev-tools libboost-dev 
    sudo apt-get python-dev python-zmq libprotobuf-dev python-protobuf
  
Create a folder for the Assisi project and position yourself there

.. code-block:: console
    
    cd ~
    mkdir assisi
    cd assisi

Dependencies
------------

Now install third-party libraries necessary for building and running
the software. First ZeroMQ:

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

Finally, install the enki simulator:

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

Building the assisi software
----------------------------

The simulator:

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
