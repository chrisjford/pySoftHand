import time, subprocess, os, signal, sys
from subprocess import Popen, PIPE

class SoftHand:
    # Open main.exe pipe and startup comms with hand:
    started = False
    process = Popen('main', stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print('subprocess started')

    def __init__(self, com_port='COM4'):
        self.startup(com_port)
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print('exiting')
        if self.started == False:
            print('exiting...')
            os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)
        else:
            self.terminate(self.getPosition())

    def __writeStep__(self, step):
        ##### Writes control command to main.exe #####
        # step = action identifier

        self.process.stdin.write('{}\n'.format(step))
        self.process.stdin.flush()
    
    def __checkConsole__(self):
        ##### Reads back messages from main.exe #####

        check = self.process.stdout.readline()
        print('from main.exe:', check)

    def setPosition(self, u):
        ##### Writes desired encoder position to main.exe. #####
        # u = encoder position (integer in range 0-19000)

        try:
            if u < 0 or u >= 19000:
                raise ValueError
            elif isinstance(u,int) == False:
                raise TypeError
        except ValueError:
            print("'u' cannot exceed range 0-19000")
        except TypeError:
            print("TypeError: 'u' must be of type int")
            sys.exit()
        else:
            self.__writeStep__(3)
            self.process.stdin.write('{}\n'.format(u))
            self.process.stdin.flush()
            time.sleep(0.001)

    def getPosition(self):
        ##### Gets encoder position which is returned as an integer #####

        self.__writeStep__(2)
        time.sleep(0.001)
        self.__writeStep__(22) 
        posn = self.process.stdout.readline()
        posn = int(posn)
        return posn

    def getCurrent(self):
        ##### Gets motor current which is returned as an integer #####

        self.__writeStep__(2)
        time.sleep(0.001)
        self.__writeStep__(23) 
        curr = self.process.stdout.readline()
        curr = int(curr)
        return curr

    def startup(self, com_port):
        ##### Startup routine #####
        # com_port = COM port to which SoftHand is assigned. Must be of type string.

        try:
            if isinstance(com_port, str) == False:
                raise ValueError
        except ValueError:
            print("'com_port' must be of type str")
            sys.exit()
            
        else:
            # Write step number to main.exe to trigger startup:
            self.__writeStep__(1)
            self.process.stdin.write('{}\n'.format(com_port))
            self.process.stdin.flush()
            time.sleep(0.001)

            # Read back checks:
            self.__checkConsole__() # 'Startup initiated...'
            self.__checkConsole__()# '1. a) Comms open'
            self.__checkConsole__() # '1. b) Motors activated'
        
        self.started = True

    def terminate(self, u):
        ##### Terminates comms and ends the program #####

        if u > 0: # Opens hand if it is partially closed at program termination
            print('------------------------------------- \n opening hand for comms closure...')
            self.setPosition(0)

            time.sleep(2)

        self.__writeStep__(4)
        print('------------------------------------- ')
        self.__checkConsole__() # 'closing comms...'
        print('Python: terminating...')
        os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)