# pySoftHand - Library for controlling and communicating with the Pisa/IIT SoftHand using Python.

This library features a selection of functions from the qbRobotics qbAPI for controlling/communicating wth the Pisa/IIT SoftHand, presented as an easy to use Python wrapper.  
  
## Contents:
**pySoftHand.py** - This is the function library and contains the SoftHand class which should be imported into your project.  
**test.py** - A short test script giving an example of home to use this library. When run, this script will open communications, partially close the SoftHand, briefly pause, then reopen and close again whilst printing out real-time encoder position updates. Finally, the script will reopen the hand and terminate comms.   
**main.exe** - Executable constructed from C++ source code taken from qbAPI.

## Instructions for use:
The source code for the functions in this library is pre-built into **main.exe** and as such it is easy to get started:  

1. Extract the contents of this folder in the root directory of your project.  
2. Plug in your SoftHand via USB and locate the port number. This should be defined as a string and passed as an input argument to the **startup()** function.  
3. To import functions, specify "from pySofthand import SoftHand" at the beginning of your program. Then, use a with statement to instantiate the class, specifying the COM port the SoftHand is on. Example of moving a SoftHand on COM4 to encoder position 7500:  
    ```python
    from pySoftHand import Softhand  
    with SoftHand("COM4") as sh:
        sh.setPosition(7500)
    ```
    A more substantial example of how to use the library is given in **test.py**.

**NOTE** - the **setPosition()** function is written such that it can be interrupted by an updated position or termination flag and also inherently runs asynchronously to the **getPosition()**/**getCurrent()** functions (as shown in **test.py**), making position feedback control of the hand quite straightforward.
