import time, subprocess
from subprocess import Popen, PIPE


class SoftHand:
    com_port = "COM 4"
    def __init__(self):
        pass

    def writeStep(self, step, process):
        ##### Writes control command to main.exe #####
        process.stdin.write('{}\n'.format(step))
        process.stdin.flush()

    def setPosition(self, u, process):
        ##### Writes desired u value to main.exe. Must be integer in range 0-19000 #####
        if u < 0 or u >= 19000:
            self.terminate(u, process)
            raise ValueError("'u' cannot exceed range 0-19000")
        elif isinstance(u,int) == False:
            self.terminate(u, process)
            raise TypeError("'u' must be of type int")
        else:
            self.writeStep(3, process)
            process.stdin.write('{}\n'.format(u))
            process.stdin.flush()
            time.sleep(0.001)

    def getPosition(self, process):
        ##### Gets encoder position which is returned as an integer #####
        self.writeStep(2, process)
        time.sleep(0.001)
        self.writeStep(22, process) 
        posn = process.stdout.readline()
        posn = int(posn)
        return posn

    def getCurrent(self, process):
        ##### Gets motor current which is returned as an integer #####
        self.writeStep(2, process)
        time.sleep(0.001)
        self.writeStep(23, process) 
        curr = process.stdout.readline()
        curr = int(curr)
        return curr

    def checkConsole(self, process):
        ##### Reads back messages from main.exe #####
        check = process.stdout.readline()
        print('from main.exe:', check)

    def startup(self, com_port):
        ##### Startup routine #####
        # Open main.exe pipe and startup comms with hand:
        process = Popen('main', stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print('subprocess started')

        # Write step number to main.exe to trigger startup:
        self.writeStep(1, process)
        process.stdin.write('{}\n'.format(com_port))
        process.stdin.flush()
        time.sleep(0.001)

        # Read back checks:
        self.checkConsole(process) # 'Startup initiated...'
        self.checkConsole(process)# '1. a) Comms open'
        self.checkConsole(process) # '1. b) Motors activated'

        # Returns subprocess details for reference to subsequent function calls:
        return process

    def terminate(self, u, process):
        ##### Terminates comms and ends the program #####

        if u > 0: # Opens hand if it is partially closed at program termination
            print('----------------------------- \n opening hand for comms closure...')
            self.setPosition(0, process)

            time.sleep(2)

        self.writeStep(4, process)

        print('----------------------------- ')
        self.checkConsole(process) # 'closing comms...'
        print('Python: terminating...')