Installation instructions for development mode
==============================================

The primary :ref:`Installation instructions`_ indicate how to install the 
assisi playground and API (`assisipy`) in user-mode.

For development purposes, it may be preferrable to install either the playground or the API (or both) directly from the github 
source.  

.. Here we provide instructions for each part independently.

**Playground** At present the main playground code is installed in this way,
so consult the primary guide.

**assisipy API** Rather than following step 3 of :ref:`Building the assisi software`_ in the primary guide, follow the steps below.



Assumptions of prior installation
---------------------------------


Here we assume that you are using Ubuntu /debian 14.04 and have the directory structure:

  * assisi

    - playground
    - examples
    - python
    - deps

      + enki

and that you have already followed the steps below from the primary guide:

  - dependencies from the standard repositories (i.e., through `apt-get`)
  - enki dependency, from github, compiled and installed / available on the system path, probably in /usr/local/include
  - assisi playground software, from github, compiled, and the executable on your system path (or added to the PATH environment variable when needed) 
     - the installation completed correctly using an up-to-date msg submodule.


The Python API
--------------

.. code-block:: console

  git clone https://github.com/larics/assisi-python python
  cd python
  git submodule update --init
  ./compile_msgs.sh
  export PYTHONPATH=${PYTHONPATH}:~/assisi/python
  cd ..

The ``PATH`` and ``PYTHONPATH`` exports have to be done very time you open a new shell, so It's best to add it to the end of your ``~/.bashrc`` file. It's purpose is to enable the importing of the Assisi python API in Python programs.


Setting up a dual-source repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two main methods that developers contribute to the assisi playground source:

1. having read-write access to https://github.com/larics/assisi-python
2. using read-only access to github/larics/assisi-python; modifying a fork, and contributing via pull requests.

To configure a repository for route #1:

.. code-block:: console

  git clone git@github.com:larics/assisi-python.git python 

  cd python
  git submodule update --init
  ./compile_msgs.sh
  export PYTHONPATH=${PYTHONPATH}:~/assisi/python
  cd ..

To configure a repository for route #2:

.. code-block:: console

  # set up your own fork with r+w
  git clone git@github.com:<GH-USER>/assisi-python.git python
  cd python
  git submodule update --init
  ./compile_msgs.sh

  # now add the remote 
  git remote add upstream https://github.com/larics/assisi-playground
  git fetch


See the github `gitflow page <https://guides.github.com/introduction/flow/>`_ for info on the workflow - in brief, in involves:

- sync your fork:master with the upstream:master
- branch from your master
- commit changes to your new feature branch
- push to your fork
- create a pull request from your fork to the upstream






