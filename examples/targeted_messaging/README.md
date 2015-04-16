
**Summary** This example shows how to use messaging between CASUs, where the
identity of a message origin is relevant to the processing.

**Expected behaviour** 
When a bee goes past a sensor facing in the direction of the centre CASU, that
CASU emits a message.

When the message is received by the central CASU, it sets the LED according to
the neighbour it was sent by.  This is set up logically, so if the behaviours
are launched: 

1. using <cfg-match>
   then we use matching colors between the hub and spokes:
   whatever color the spoke flashes, the hub should (approx) simultaneously
   flash the same color. (red from the left, green from the right).
2. using <cfg-diff> 
   then we use differing colors between the hub and spokes:
   whatever color the spoke flashes, the hub should (approx) simultaneously
   flash the other color. (green from the left, red from the right).

The examples illustrate that the connection (label) in the receiving CASU can be redefined easily, while the physical setup (port/host IP) need not be changed -- or indeed could be changed independently.

# How to run
1. start the simulator
cd <wherever>
./assisi_playground

2. spawn the objects
<run in this directory>
python ./spawn_casus_bees.py

3. run behaviour of bees
- there is just one script for both bees.
python bees_circling.py 


4. run CASU controllers -- in different terminals (or backgrounded)
(set 1):
python hub.py   --rtc-path cfg-diff --name casu-ctr
python spoke.py --rtc-path cfg-diff --name casu-right -d W
python spoke.py --rtc-path cfg-diff --name casu-left -d E

(set 2):
python hub.py   --rtc-path cfg-match --name casu-ctr
python spoke.py --rtc-path cfg-match --name casu-right -d W
python spoke.py --rtc-path cfg-match --name casu-left  -d E

5. once done, <ctrl-c> should shut down the handlers gracefully
(sometimes interaction with the threading library means it doesn't)

*Note*: shut down clients first, then kill the assisi playground.

 

# History
April 2015 : Extended idea from `messaging`, to validate specific messaging.



