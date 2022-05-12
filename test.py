import time
from pySoftHand import SoftHand

u = 15000 # Target encoder position (range 0-19000)

#sh = SoftHand() # Instantiate instance of SoftHand class
with SoftHand("COM4") as sh:

    ### SIMPLE OPEN/CLOSE DEMO ###

    sh.setPosition(u) # Moves SoftHand to given encoder position 'u' on the process defined in the startup function.
    time.sleep(2) # Wait for command to complete...
    sh.setPosition(0) # Open hand
    time.sleep(2) # Wait for command to complete...

    ### ASYNCHRONOUS POSITION FEEDBACK DEMO ###

    sh.setPosition(u) # Tell SoftHand to move to encoder position 'u'.
    t_0 = time.perf_counter() # Timer...
    t_1 = 0

    # While loop prints live encoder position updates as SoftHand closes
    while t_1 < 3:
        t_1 = time.perf_counter() - t_0
        posn = sh.getPosition()
        print(f'encoder position is {posn}')
        time.sleep(0.001)