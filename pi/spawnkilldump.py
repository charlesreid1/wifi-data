import subprocess
import time

print "\n"
print "Don't forget to run this program as root.\n"
print "Don't forget to put your wireless card in monitor mode.\n"

for i in range(10):

    print "Beginning round",i+1,"of 10"

    Nmin = 1
    Nsec = Nmin*60

    the_cmd = ['airodump-ng','wlan0','-w','awesome','--output-format','csv','-M','-u','30']#,'--berlin','%d'%(Nsec),'wlan1']

    print " ".join(the_cmd)

    p = subprocess.Popen(the_cmd)

    time.sleep(Nsec)
    p.kill()

    print "Success!"


