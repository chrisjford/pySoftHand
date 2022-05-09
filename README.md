# pySoftHand - library for controlling and communicating with the Pisa/IIT SoftHand using Python.

This library features a selection of functions from the qbRobotics qbAPI for controlling/communicating wth the Pisa/IIT SoftHand, presented in an easy to use Python wrapper.  
  
## Contents:
**pySoftHand.py** - This is the function library and contains the SoftHand class which should be imported into your project.
**test.py** - A short test script giving an example of home to use this library. When run, this script will open communications, partially close the SoftHand, briefly pause, then reopen and terminate comms. 
**main.exe** - Executable constructed from C++ source code taken from qbAPI.

## Instructions for use:

1. Place this folder in the root directory of your project.
2. Plug in your SoftHand via USB and locate the port number. This should be defined as a string and passed as an input argument to the startup() function.
3. To import functions, specify "from pySoftHand.pySofthand import SoftHand" at the beginning of your program. Functions from the SoftHand class can then be called as in *test.py*.
  **NOTE** - the setPosition() function is written such that it can be interrupted by an updated position or termination flag and also inherently runs asynchronously to the getPosition()/getCurrent() functions (as shown in *test.py*), making position feedback control of the hand quite straightforward.