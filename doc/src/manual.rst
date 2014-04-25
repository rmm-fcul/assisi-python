Manual Casu control
===================

The assisipy library can be used to manually control one or several
casus from the interactive Python interpreter. For convenience, we
suggest using the `IPython <http://ipython.org>`_ environment, because it provides some nice
features, such as tab-completion, a command history etc.

Prerequisites
-------------

The IPython library needs to be installed manually. It's provided in
Ubuntu's official repositories, so installing it is as simple as

.. code-block:: console

   $ sudo apt-get install ipython


An example control session
--------------------------

The rest of this document is a walk-through a basic manual control
session. It can be done using either a simulated, or a real Casu. 

To get started, position yourself in the examples/logging folder and
start ipython there:

.. code-block:: console

   $ cd ~/assisi/python/examples/logging
   $ ipython


Spawning the simulated Casu
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming you have the simulator running, import the simulator
API and spawn a Casu:

.. code-block:: ipython

   In[1]: from assisipy import sim
   In[2]: s = sim.Control()
   In[3]: s.spawn('Casu','casu-004_sim',(0,0,0))
   
Setting up the real Casu
~~~~~~~~~~~~~~~~~~~~~~~~

Since the manual control will be run **locally**, you do *not* need to
go through all the steps described in :doc:`deploy`. All you need to
do is power up the Casu and its control board.

Control commands
~~~~~~~~~~~~~~~~

Now we are ready to control the Casu. Import the Casu API:

.. code-block:: ipython

   In[4]: from assisipy import casu

In order to run the manual controller, you need to have the
appropriate :ref:`.rtc file <rtc_structure>` for the Casu that you
are trying to control. Examples can be found in the
``assisi/python/examples/logging`` folder.

For the simulated casu, run:

.. code-block:: ipython

   In[5]: casu4 = casu.Casu('casu-004_sim.rtc', log =  True, log_folder = 'logs')
   
For controlling the real Casu, simply supply the appropriate ``.rtc``
file:

.. code-block:: ipython

   In[5]: casu4 = casu.Casu('casu-004.rtc', log = True, log_folder = 'logs')

Note that the ``log_folder`` has to be created in advance (it will not
be created automatically). If everything went ok, you will see a message:

.. code-block:: ipython

   ## casu-004 connected!

If you don't see the message, the controller was not able to connect
to the designated Casu. The most common cause of connection problems
is incorrect ``.rtc`` file configuration. Doublecheck the `name`, `pub_addr`
and `sub_addr` parameters.

After successfully connecting, you can issue commands to directly control the casu actuators. For
instance, to light the top diagnostic LED red and turn on the vibration motor:

.. code-block:: ipython

   In[6]: casu4.set_diagnostic_led_rgb(r=1)
   In[7]: casu4.set_vibration_frequency(50)

To issue several commands simultaneously, simply write them in one
line, separated by semicolons. For instance, let's turn off the
diagnostic LED and turn on the light stimulus at the same time:

.. code-block:: ipython

   In[8]: casu4.diagnostic_led_standby(); casu4.set_light_rgb(b=1)

There is no limit to the number of commands you can concatenate in
this way.

To help you with typing the rather verbose function names, IPython
supports *tab completion*. Just start typing the first few
letters, then press the ``Tab`` key, and IPython will automatically
complete the function name.

In a similar way, we can also control the heat actuator:

.. code-block:: ipython

   In[9]: casu4.set_temp(20); casu4.set_diagnostic_led_rgb(r=1)


TODO: Add instructions for the EM actuators

You can also check the current value of any sensor, e.g. for the
"northern" proximity sensor:

.. code-block:: ipython

   In[10]: casu4.get_ir_raw_value(casu.IR_N)

For a full list of available functions, and detailed explanation of
function arguments, please consult the :py:mod:`casu` documentation.

Controlling several Casus at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to issue several commands at once, you can use the same
command concatenation technique discussed earlier.

If you are following the simulated example, spawn another casu and
start up its controller:

.. code-block:: ipython

   In[11]: s.spawn('Casu','casu-003_sim',(3,0,0))
   In[12]: casu3 = casu.Casu('casu-003_sim.rtc',log = True, log_folder = 'logs')

If you are working with real casus, just make sure the target casu is turned on and
connected to the network.

Now you can issue commands to both casus at once:

.. code-block:: ipython

   In[13]: casu4.set_diagnostic_led_rgb(g = 1); casu3.set_diagnostic_led_rgb(r = 1)

other commands work equivalently.

Stopping the casus
~~~~~~~~~~~~~~~~~~

This step is **important** because it will make sure all the Casu
actuators have been turned off, and the log files have been written to
and closed appropriately.

After finishing the experiment, stop the Casus and clean up the
control variables:

.. code-block:: ipython

   In[14]: casu3.stop(); casu4.stop()
   In[15]: del casu3, casu4

Analyzing the logs
~~~~~~~~~~~~~~~~~~

The log files generated by the casu class aggregate all of the
available sensor and actuator data into a single ``.csv`` file. A
utility library is provided for splitting this into separate
per-device log files. It is invoked as:

.. code-block:: ipython
   
   In[16]: from assisipy.tools import logtools
   In[17]: logtools.split('log file name')

