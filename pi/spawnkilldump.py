import subprocess
import time

print "\n"
print "Don't forget to run this program as root.\n"

interval = 30

monitor1 = ['ifconfig','wlan0','down']
monitor2 = ['iwconfig','wlan0','mode','monitor']
monitor3 = ['ifconfig','wlan0','up']

subprocess.call(monitor1)
subprocess.call(monitor2)
subprocess.call(monitor3)

print "Don't forget to put your wireless card in monitor mode.\n"

for i in range(10):

    print "Beginning round",i+1,"of 10"

    the_cmd = ['airodump-ng','wlan0','-w','awesome','--output-format','csv','-M']#,'--berlin','%d'%(Nsec),'wlan1']

    print " ".join(the_cmd)

    p = subprocess.Popen(the_cmd)

    time.sleep(interval)
    p.kill()

    print "Success!"


