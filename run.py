import subprocess
import signal
import os
from subprocess import Popen, PIPE, STDOUT 
import numpy as np
import time
import keyboard

# Main function:
def run():
    flag = True # While loop flag
    ready = False # Startup routine flag
    step = 0 # Step variable
    x = 0 # Hand closure variable
    lim = 19000 # Hand closure limit - DO NOT EXCEED 19000
    increment = 500 # Defines how many encoder steps are moved per cycle
    pause = 0.025 # Refresh time

    print('running... \n')


    while flag == True:

        ############ STARTUP ROUTINE ##############
        if ready == False:
            step = 1
            
            # Write step number to executable to trigger startup:
            process.stdin.write('{}\n'.format(step))
            process.stdin.flush()

            # Read back checks:
            check = process.stdout.readline()
            print('from main.exe:', check) # 'Startup initiated...'

            check = process.stdout.readline()
            print('from main.exe:', check) # '1. a) Comms open'

            check = process.stdout.readline()
            print('from main.exe:', check) # '1. b) Motors activated'

            ready = True # Allows opening and closing routines

        ############ CLOSE HAND ##############
        if keyboard.is_pressed('2') and ready and x < lim:
            x = (x + increment) # Update encoder value
            step = 2
            
            # Initiate closing function:
            process.stdin.write('{}\n'.format(step))
            process.stdin.flush()

            # Write updated position to hand:
            process.stdin.write('{}\n'.format(x))
            process.stdin.flush()

            time.sleep(pause) # Pause for debounce

        ############ OPEN HAND ##############
        if keyboard.is_pressed('3') and ready:
            x = (x - increment) # Update encoder value
            step = 3
            
            # Initiate opening function:
            process.stdin.write('{}\n'.format(step))
            process.stdin.flush()

            # Write updated encoder position to hand:
            process.stdin.write('{}\n'.format(x))
            process.stdin.flush() 

            time.sleep(pause) # Pause for debounce

        ############ EXIT ROUTINE ##############
        if keyboard.is_pressed('esc'):
            if x > 0: # Opens hand if it is partially closed at program termination
                x = 0
                step = 4
                print('----------------------------- \n opening hand for comms closure...')
                process.stdin.write('{}\n'.format(step))
                process.stdin.flush()
                time.sleep(2)

            step = 5
    
            process.stdin.write('{}\n'.format(step))
            process.stdin.flush()

            print('----------------------------- ')
            check = process.stdout.readline()
            print('from main.exe:', check) # 'closing comms...'

            print('Python: terminating...')
            flag = False # End while loop
               
# Start main.exe:
process = Popen('main', stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

# Run main loop:
run()

# End process:
os.kill(process.pid, signal.CTRL_BREAK_EVENT)