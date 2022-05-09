# pySoftHand - Library for controlling and communicating with the Pisa/IIT SoftHand using Python.

This library features a selection of functions from the qbRobotics qbAPI for controlling/communicating wth the Pisa/IIT SoftHand, presented as an easy to use Python wrapper.  
  
## Contents:
**pySoftHand.py** - This is the function library and contains the SoftHand class which should be imported into your project.  
**test.py** - A short test script giving an example of home to use this library. When run, this script will open communications, partially close the SoftHand, briefly pause, then reopen and terminate comms.   
**main.exe** - Executable constructed from C++ source code taken from qbAPI.

## Instructions for use:
The source code for the functions in this library is pre-built into **main.exe** and as such it is easy to get started:  

1. Place this folder in the root directory of your project.  
2. Plug in your SoftHand via USB and locate the port number. This should be defined as a string and passed as an input argument to the **startup()** function.  
3. To import functions, specify "from pySoftHand.pySofthand import SoftHand" at the beginning of your program. An instance of the SoftHand class should be created here also:  
    ```python
    from pySoftHand.pySoftHand import Softhand  
    sh = SoftHand()  # Instantiate SoftHand class
    com_port = "COM4" # Define COM port
    ```
5. The **startup()** function should then be called and assigned to a variable (conventionally named **process**). This is done as the function returns information on the subprocess on which **main.exe** is subscribed to. As such, **process** is required to be passed as an input argument to all subsequent functions from the SoftHand class:
    ```python
    process = sh.startup(com_port)
    sh.setPosition(10000, process)
    ```
    A more substantial example of how to use the library is given in **test.py**.

**NOTE** - the **setPosition()** function is written such that it can be interrupted by an updated position or termination flag and also inherently runs asynchronously to the **getPosition()**/**getCurrent()** functions (as shown in **test.py**), making position feedback control of the hand quite straightforward.
