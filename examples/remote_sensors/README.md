**Summary** This example shows CASUs communicating across multiple different
arenas, which are hosted within different simulator environments.  It is
intended that those simulators are run on different computers (and therefore
demonstrating long-range interactions), but is parameterisable to use two
instances on the same computer.

**The setup**

Arena A: 2 CASUs and 2 bees.  Bees follow simple trajectory around each CASU,
triggering IR sensors periodically.  Consider these CASUs as "sensors", which
emit a message to the CASU in arena B.

Arena B: 1 CASU. Consider this CASU a "display"/"aggregator".  It changes the
LED color to reflect the inputs from the other CASUs.

black / off (neither) 
red (left triggered) 
green (right triggered)
yellow (both triggered)

**Expected behaviour** Since the two bees move at different rates, the two
sensor CASUs are sometimes triggered together and other times separately.
Thus, the aggregator CASU will cycle through all four colors.


**How to run**

There is a small shell script that launches all of the necessary programs
(simulator, spawning of agents, CASU and bee behaviours).
It takes a single argument, which indicates whether arena A or arena B is
being launched.

Before executing, one should set up the desired addresses, and three paths.
These are all setup in "launch.sh", in about the top 25 lines.
Note: the ip:port pairs should all be unique, which include these scenarios:

i) one machine
ipA=ipB; then saA!=saB, paA!=paB
ii) two machines
ipA!=ipB; then it is possible (but not required) for saA=saB, paA=paB

Later variants should include where the simulators are hosted on two 
machines, and the CASU controllers are not hosted on the machine that 
matches the location of the relevant simulator.  These should be setup
using different settings for ``rtcpath``



For visibility of the process, each stage can also be executed manually:

1. launch both instances of the simulator
2. spawn the objects
3. run bees behaviour (A only)
4. run CASU behaviour (A -- sensors)
5. run CASU behaviour (B -- aggregator)
6. observe, send bug reports....
