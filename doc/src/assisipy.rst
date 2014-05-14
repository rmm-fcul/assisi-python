assisipy Package
================

:mod:`assisipy` Package
-----------------------

.. automodule:: assisipy.__init__
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`bee` Module
-----------------

.. automodule:: assisipy.bee
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`casu` Module
------------------

.. automodule:: assisipy.casu
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`physical` Module
----------------------

.. automodule:: assisipy.physical
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`sim` Module
-----------------

.. automodule:: assisipy.sim
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`examples` Module
----------------------


Wandering bee example
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/wandering_bee/spawn_bee_in_maze.py
.. literalinclude:: ../../examples/wandering_bee/bee_wander.py

Casu and bee example
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/casu_proxy_led/spawn_casu_and_bee.py
.. literalinclude:: ../../examples/casu_proxy_led/casu_proxy_led.py
.. literalinclude:: ../../examples/casu_proxy_led/bee_circling.py

Heat test
~~~~~~~~~

Start the simulator (it must be started from the same folder where the
simulator executable is located!)

From the ``examples/heat_test`` folder run

.. code-block:: console
                
    $ ./spawn_casu_and_be.py
    $ ./casu_heat_switch.py

In a new console window, run:

.. code-block:: console

    $ ./bee_wander_straight.py

The casu will be toggling its peltier actuator between heating and
cooling every two minutes. The bee will be printing its temperature
sensor value, while wandering in straight lines
from one end of the arena to the other.
