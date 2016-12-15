.. _other-platforms-label:

Installation instructions for other platfoms
=================================================

The following Operating Systems are not officially supported. This
means that the sotware is not tested regularly on these systems. Use
at your own risk.

Mac OS X
--------

Storage requirements: about 1GB (600MB for QT)

- make a directory ~/assisi/deps


Python library stuff:
~~~~~~~~~~~~~~~~~~~~~~~

- install git as pkg for MacOS (mentions SnowLeopard, but works on Lion & Mavericks) from sourceforge: http://sourceforge.net/projects/git-osx-installer/files/latest/download
- if missing: get „pip“
- sudo pip install pyzmq
- sudo pip install sphinx
- sudo pip install yaml

Protobuf:
~~~~~~~~~~~
- goto folder ~/assisi/deps
- There, download propotobuf version 2.5 from https://code.google.com/p/protobuf/downloads/detail?name~protobuf-2.5.0.zip&can~2&q~
- unpack it, go into that directory
- ./configure
- make
- sudo make install
- sudo pip install protobuf


QT:
~~~~~
- download QT4.8.x libraries for MAcOS from: http://qt-project.org/downloads
- install these QT libraries (installer program)


ZeroMQ library:
~~~~~~~~~~~~~~~~~
- curl -OL http://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz
- tar -xzf autoconf-2.69.tar.gz 
- cd autoconf-2.69
- ./configure && make && sudo make install
 
- curl -OL http://ftpmirror.gnu.org/automake/automake-1.14.tar.gz
- tar -xzf automake-1.14.tar.gz
- cd automake-1.14
- ./configure && make && sudo make install
 
- curl -OL http://ftpmirror.gnu.org/libtool/libtool-2.4.2.tar.gz
- tar -xzf libtool-2.4.2.tar.gz
- cd libtool-2.4.2
- ./configure && make && sudo make install

- Go back to folder ~/assisi/deps
- download zeromq 3.x. from: http://zeromq.org/intro:get-the-software
- unpack it in a folder in ~/assisi/deps
- change to that folder
- ./autogen.sh
- ./configure     # add other options here
- make
- make check
- sudo make install



ZeroMQ headers:
~~~~~~~~~~~~~~~~~
- goto ~/assisi/deps
- git clone https://github.com/zeromq/cppzmq
- sudo cp cppzmq/zmq.hpp /usr/local/include

libboost:
~~~~~~~~~~~

- Download lib boost from: http://sourceforge.net/projects/boost/files/boost/1.50.0/boost_1_50_0.tar.gz/download
- Place it into ~/assisi/deps
- tar -xzf boost_1_50_0.tar.gz
- cd boost_1_50_0
- ./bootstrap.sh --prefix~/usr/local
- ./b2
- sudo ./b2 install


PATH issues:
~~~~~~~~~~~~~~
- add the ~/assisi/python directory to PYTHONPATH: „export PYTHONPATH~${PYTHONPATH}:~/assisi/python“


enki:
~~~~~~~
- make sure you are in ~/assisi/deps
- download the macOS cake pkg from: http://www.cmake.org/cmake/resources/
software.html
- accept the question for „install command line links“ (/usr/bin)
- git clone https://github.com/larics/enki
- cd enki
- mkdir build
- cd build
- open ~/assisi/deps/enki/build/viewer/viewer.cpp in the editor
- change in line 10: #include <GL/glu.h> to #include <OpenGL/glu.h>
- cmake ..
- make
- sudo make install
- cd ../../..

playground:
~~~~~~~~~~~~~
- switch to ~/assisi
- git clone https://github.com/larics/assisi-playground playground
- cd playground
- git submodule update --init
- mkdir build
- cd build

- cmake .. (This will fail, but we need it to generate the CMakeCache.txt)

- You should get an error that libZMQ is not found. Edit
  CMakeCache.txt and put "/usr/local/include" to the
  ZMQ_INCLUDE_DIR. It should look like this:

.. code-block:: cmake
    ////////////////////////////////////////////////////
    //Path to a file.
    ZeroMQ_INCLUDE_DIR:PATH~/usr/local/include
    //Path to a library.
    ZeroMQ_LIBRARY:FILEPATH~/usr/local/lib/libzmq.dylib
    ///////////////////////////////////////////////////

- cmake .. (do it again, now it should work)

- Now it should run through, however it still complains that package libzmq is not found, although  ZMQ_LIB_DIR points to /usr/local/lib where those lib files are.

- make
- cd ../..

python-simulator-stuff:
~~~~~~~~~~~~~~~~~~~~~~~~~
- switch to ~/assisi
- git clone https://github.com/assisi/assisipy python
- cd python
- git submodule update --init
- ./compile_msgs.sh
- export PYTHONPATH~${PYTHONPATH}:~/assisi/python
- cd ..



build the documentation of assisi-py:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- change to ~/Documents/python
- git submodule update --init
- ./compile_msgs.sh
- ./compile_docs.sh

Now the doc is in ./docs/html/index.html

Ubuntu 14.04 (Trusty) 64-bit
----------------------------

Trusty was the officially supported platform up until
December 2016. At the time of writing (December 2016), the official
(Xenial) installation instructions are known to work for
Trusty. However, as Trusty is not actively maintained any more, you
are encouraged to move to Xenial at your earliest convenience.

Ubuntu 12.04 Precise Pangolin
-----------------------------

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


.. _upgrading-label:
Upgrading from a previous installation
======================================

When upgrading your assisi system (e.g. after an OS upgrade), it is
necessary to reinstall both Enki and the Playground.

If you have a manually installed version of libzmq on your system, you
will have to uninstall it manually. Go to the folder where you
originally built it and run ``make uninstall``

TODO: provide better instructions here...
