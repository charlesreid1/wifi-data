import subprocess
import os
import time
from datetime import datetime

script_name = "Aircrack.py"

# each experiment will be Nhours in duration
Nhours = 2

# each CSV file will be Nseconds in duration
Nseconds = 15
 
# figure out how many files there will be 
Nfiles = (Nhours*3600)/Nseconds

# create a unique file prefix for this experiment
prefix = datetime.now().strftime('%Y-%m-%d_%H-%m')

print("[%s] About to put card in monitor mode."%(script_name) )
subprocess.call(['ifconfig','wlan0','down'])
subprocess.call(['iwconfig','wlan0','mode','monitor'])
subprocess.call(['ifconfig','wlan0','up'])
print "Done."

for i in range(Nfiles):

    # construct the airodump command and pipe all its output to /dev/null so it doesn't blow up the syslog
    FNULL = open(os.devnull,'w')
    the_cmd = ['airodump-ng','wlan0','-w',prefix,'--output-format','csv']
 
    # call it
    p = subprocess.Popen(the_cmd,stdout=FNULL, stderr=subprocess.STDOUT)
 
    # wait for it
    time.sleep(Nseconds)

    # aaaaand bail 
    p.kill()
 
print("[%s] Success!"%s(script_name) )
