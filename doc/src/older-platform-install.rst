Installation instructions for older distributions
=================================================

Installations on distributions in ubuntu 12.04 are less often used and 
accordingly latest features are not tested to the same degree.  We 
retain the full instructions for installation here.

Most of the dependencies needed to build and run ASSISI software can
be installed from official Ubuntu repositories:

.. code-block:: console
  
    sudo apt-get install build-essential git cmake qt4-dev-tools
    sudo apt-get install libboost-dev libboost-program-options-dev libboost-system-dev
    sudo apt-get install libboost-filesystem-dev libboost-python-dev
    sudo apt-get install libprotobuf-dev protobuf-compiler python-protobuf
    sudo apt-get install python-dev python-sphinx python-yaml
    sudo apt-get install python-pygraphviz fabric

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

Now install python-zmq using pip (if you install using apt-get it will install an older version of libzmq as a dependency):

.. code-block:: console
  
    sudo apt-get install pip
    sudo pip install pyzmq


