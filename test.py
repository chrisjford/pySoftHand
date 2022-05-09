import time
from pySoftHand import SoftHand

u = 15000 # Target encoder position (range 0-19000)

com_port = "COM4" # Set COM port 

sh = SoftHand() # Instantiate SoftHand class

process = sh.startup(com_port) # Initiates communication with the SoftHand on the specified COM port. This variable must be called with all subsequent SoftHand funcitons.

### SIMPLE OPEN/CLOSE DEMO ###

sh.setPosition(u, process) # Moves SoftHand to given encoder position 'u' on the process defined in the startup function.
time.sleep(2) # Wait for command to complete...
sh.setPosition(0, process) #Open hand
time.sleep(2) #Wait for command to complete...

### ASYNCHRONOUS POSITION FEEDBACK DEMO ###

sh.setPosition(u, process) # Tell SoftHand to move to encoder position 'u'.
t_0 = time.perf_counter() # Timer...
t_1 = 0

# While loop prints live encoder position updates as SoftHand closes
while t_1 < 3:
    t_1 = time.perf_counter() - t_0
    posn = sh.getPosition(process)
    print(f'encoder position is {posn}')
    time.sleep(0.001)

sh.terminate(u, process) # Opens hand fully and closes comms.