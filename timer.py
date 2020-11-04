import time
import os
import playsound as ps
import sys

class WindowsInhibitor:
    '''Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx'''
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002

    def __init__(self):
        pass

    def inhibit(self):
        import ctypes
        print("Preventing Windows from going to sleep / display going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED | \
            WindowsInhibitor.ES_DISPLAY_REQUIRED)

    def uninhibit(self):
        import ctypes
        print("Allowing Windows to go to sleep / allowing the display to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)

#path to the python file
path = os.path.dirname(os.path.realpath(__file__))

def chime():
    ps.playsound(path + os.sep + "dong.wav", block=False)

timer_time_hours = 2 #number of hours to countdown
timer_time_seconds = timer_time_hours * 60 * 60

start_time = time.time()

osSleep = None # in Windows, prevent the OS from sleeping while we do our test
if(os.name == 'nt'):
    osSleep = WindowsInhibitor()
    osSleep.inhibit()

print('\r\n')

while (timer_time_seconds >= (int(time.time() - start_time))):
    try:
        all_seconds = timer_time_seconds - int(time.time() - start_time)
        
        seconds = int(all_seconds % 60)
        minutes = int(((all_seconds - seconds) / 60) % 60)
        hours = int((all_seconds - (minutes * 60 + seconds)) / 60 / 60) 


       

        sys.stdout.flush()
        sys.stdout.write("\r{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

        #chime at each of the six questions so 20 minutes per question (1200 seconds)
        if (all_seconds % 1200 == 0):
            chime()
        
        #chime for the last four seconds
        if (all_seconds < 5):
            chime()

        time.sleep(1)

    except(KeyboardInterrupt, SystemExit):
        break

print('\r\n')
#loop ended sucessfully (or Control-C pressed) - uninhibit sleep function
if osSleep:
    osSleep.uninhibit()