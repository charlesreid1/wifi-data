import subprocess
import time

print "\nDon't forget to run this program as root.\n"

for i in range(3):

    print "Beginning round",i+1,"of 10"

    Nmin = 2
    Nsec = Nmin*60

    the_cmd = ['airodump-ng','wlan1','-w','awesome','--output-format','csv','-M','-u','30']#,'--berlin','%d'%(Nsec),'wlan1']

    print " ".join(the_cmd)
    #print the_cmd

    p = subprocess.Popen(the_cmd)

    time.sleep(Nsec)
    p.kill()

    print "Success!"


