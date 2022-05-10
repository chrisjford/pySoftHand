import time, subprocess, os, signal
from subprocess import Popen, PIPE

class SoftHand:
    def __init__(self):
        pass

    def __writeStep__(self, step, process):
        ##### Writes control command to main.exe #####
        # step = action identifier
        # process = variable assigned to startup() function

        process.stdin.write('{}\n'.format(step))
        process.stdin.flush()
    
    def __checkConsole__(self, process):
        ##### Reads back messages from main.exe #####
        # process = variable assigned to startup() function

        check = process.stdout.readline()
        print('from main.exe:', check)

    def setPosition(self, u, process):
        ##### Writes desired encoder position to main.exe. #####
        # u = encoder position (integer in range 0-19000)
        # process = variable assigned to startup() function

        if u < 0 or u >= 19000:
            self.terminate(u, process)
            raise ValueError("'u' cannot exceed range 0-19000")
        elif isinstance(u,int) == False:
            self.terminate(u, process)
            raise TypeError("'u' must be of type int")
        else:
            self.__writeStep__(3, process)
            process.stdin.write('{}\n'.format(u))
            process.stdin.flush()
            time.sleep(0.001)

    def getPosition(self, process):
        ##### Gets encoder position which is returned as an integer #####
        # process = variable assigned to startup() function

        self.__writeStep__(2, process)
        time.sleep(0.001)
        self.__writeStep__(22, process) 
        posn = process.stdout.readline()
        posn = int(posn)
        return posn

    def getCurrent(self, process):
        ##### Gets motor current which is returned as an integer #####
        # process = variable assigned to startup() function

        self.__writeStep__(2, process)
        time.sleep(0.001)
        self.__writeStep__(23, process) 
        curr = process.stdout.readline()
        curr = int(curr)
        return curr

    def startup(self, com_port):
        ##### Startup routine #####
        # com_port = COM port to which SoftHand is assigned. Must be of type string.
        if isinstance(com_port, str) == False:
            raise ValueError("'com_port' must be of type str")

        # Open main.exe pipe and startup comms with hand:
        process = Popen('main', stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print('subprocess started')

        # Write step number to main.exe to trigger startup:
        self.__writeStep__(1, process)
        process.stdin.write('{}\n'.format(com_port))
        process.stdin.flush()
        time.sleep(0.001)

        # Read back checks:
        self.__checkConsole__(process) # 'Startup initiated...'
        self.__checkConsole__(process)# '1. a) Comms open'
        self.__checkConsole__(process) # '1. b) Motors activated'

        # Returns subprocess details for reference to subsequent function calls:
        return process

    def terminate(self, u, process):
        ##### Terminates comms and ends the program #####

        if u > 0: # Opens hand if it is partially closed at program termination
            print('----------------------------- \n opening hand for comms closure...')
            self.setPosition(0, process)

            time.sleep(2)

        self.__writeStep__(4, process)

        print('----------------------------- ')
        self.__checkConsole__(process) # 'closing comms...'
        print('Python: terminating...')
        os.kill(process.pid, signal.CTRL_BREAK_EVENT)