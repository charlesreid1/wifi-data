'''
Slightly modified version of Dan McInerney's script wifijammer

https://github.com/DanMcInerney/wifijammer

From Dan McInerney:

Copyright (c) 2014, Dan McInerney All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    Neither the name of Dan McInerney nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb = 0
import os
import sys
import time
from threading import Thread, Lock
from subprocess import Popen, PIPE
from signal import SIGINT, signal
import argparse
import socket
import struct
import fcntl

W = '\033[0m'  # white (normal)
R = '\033[31m' # red
G = '\033[32m' # green
O = '\033[33m' # orange
C = '\033[36m' # cyan
T = '\033[93m' # tan

def parse_args():
	#Create the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i","--interface", help="Choose monitor mode interface. By default script will find the most powerful interface and starts monitor mode on it. Example: -i mon5")
    parser.add_argument("-c","--channel",   help="Listen on and deauth only clients on the specified channel. Example: -c 6")
    parser.add_argument("-a","--accesspoint", help="MAC of specific access point")
    parser.add_argument("--world", help="N. American standard is 11 channels but the rest of the world it's 13 so this options enables the scanning of 13 channels", action="store_true")

    return parser.parse_args()




########################################
# Begin interface settings
########################################

def get_mon_iface(args):
    global monitor_on
    monitors, interfaces = iwconfig()
    if args.interface:
        monitor_on = True
        return args.interface
    if len(monitors) > 0:
        monitor_on = True
        return monitors[0]
    else:
        # Start monitor mode on a wireless interface
        print '['+G+'*'+W+'] Finding the most powerful interface...'
        interface = get_iface(interfaces)
        monmode = start_mon_mode(interface)
        return monmode


def iwconfig():
    monitors = []
    interfaces = {}
    try:
        proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
    except OSError:
        sys.exit('['+R+'-'+W+'] Could not execute "iwconfig"')
    for line in proc.communicate()[0].split('\n'):
        if len(line) == 0: continue # Isn't an empty string
        if line[0] != ' ': # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search: # Isn't wired
                iface = line[:line.find(' ')] # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    return monitors, interfaces


def get_iface(interfaces):
    scanned_aps = []

    if len(interfaces) < 1:
        sys.exit('['+R+'-'+W+'] No wireless interfaces found, bring one up and try again')
    if len(interfaces) == 1:
        for interface in interfaces:
            return interface

    # Find most powerful interface
    for iface in interfaces:
        count = 0
        proc = Popen(['iwlist', iface, 'scan'], stdout=PIPE, stderr=DN)
        for line in proc.communicate()[0].split('\n'):
            if ' - Address:' in line: # first line in iwlist scan for a new AP
               count += 1
        scanned_aps.append((count, iface))
        print '['+G+'+'+W+'] Networks discovered by '+G+iface+W+': '+T+str(count)+W
    try:
        interface = max(scanned_aps)[1]
        return interface
    except Exception as e:
        for iface in interfaces:
            interface = iface
            print '['+R+'-'+W+'] Minor error:',e
            print '    Starting monitor mode on '+G+interface+W
            return interface

def start_mon_mode(interface):
    print '['+G+'+'+W+'] Starting monitor mode off '+G+interface+W
    try:
        os.system('ifconfig %s down' % interface)
        os.system('iwconfig %s mode monitor' % interface)
        os.system('ifconfig %s up' % interface)
        return interface
    except Exception:
        sys.exit('['+R+'-'+W+'] Could not start monitor mode')

def remove_mon_iface(mon_iface):
    os.system('ifconfig %s down' % mon_iface)
    os.system('iwconfig %s mode managed' % mon_iface)
    os.system('ifconfig %s up' % mon_iface)


def mon_mac(mon_iface):
    '''
    http://stackoverflow.com/questions/159137/getting-mac-address
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', mon_iface[:15]))
    mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    print '['+G+'*'+W+'] Monitor mode: '+G+mon_iface+W+' - '+O+mac+W
    return mac

########################################
# End interface settings
########################################




########################################
# Set channel hop behavior
########################################


def channel_hop(mon_iface, args):
    '''
    First time through, scan each channel for 5 seconds.
    Then skip through all channels quickly.
    '''

    global monchannel, first_pass

    channelNum = 0
    maxChan = 11 if not args.world else 13
    err = None

    while 1:
        if args.channel:
            with lock:
                monchannel = args.channel
        else:
            channelNum +=1
            if channelNum > maxChan:
                channelNum = 1
                with lock:
                    first_pass = 0
            with lock:
                monchannel = str(channelNum)

            try:
                proc = Popen(['iw', 'dev', mon_iface, 'set', 'channel', monchannel], stdout=DN, stderr=PIPE)
            except OSError:
                print '['+R+'-'+W+'] Could not execute "iw"'
                os.kill(os.getpid(),SIGINT)
                sys.exit(1)
            for line in proc.communicate()[1].split('\n'):
                if len(line) > 2: # iw dev shouldnt display output unless there's an error
                    err = '['+R+'-'+W+'] Channel hopping failed: '+R+line+W

        output(err, monchannel)
        if args.channel:
            time.sleep(.05)
        else:
            # For the first channel hop thru, do not deauth
            if first_pass == 1:
                time.sleep(1)
                continue



########################################
# End channel hop behavior
########################################







########################################
# Set output filtering
########################################

def output(err, monchannel):
    ### #
    ### # cmr:
    ### # print out information/records as they are added to the db 
    ### #
    ### os.system('clear')
    ### if err:
    ###     print err
    ### else:
    ###     print '['+G+'+'+W+'] '+mon_iface+' channel: '+G+monchannel+W+'\n'
    ### if len(clients_APs) > 0:
    ###     print '                  Clients                   ch   ESSID'
    ### # Print the clients list
    ### with lock:
    ###     for ca in clients_APs:
    ###         if len(ca) > 3:
    ###             print '['+T+'*'+W+'] '+O+ca[0]+W+' - '+O+ca[1]+W+' - '+ca[2].ljust(2)+' - '+T+ca[3]+W
    ###         else:
    ###             print '['+T+'*'+W+'] '+O+ca[0]+W+' - '+O+ca[1]+W+' - '+ca[2]
    ### if len(APs) > 0:
    ###     print '\n      Access Points     ch   ESSID'
    ### with lock:
    ###     for ap in APs:
    ###         print '['+T+'*'+W+'] '+O+ap[0]+W+' - '+ap[1].ljust(2)+' - '+T+ap[2]+W
    ### print ''
    pass



def noise_filter(addr1, addr2):
    ignore = ['ff:ff:ff:ff:ff:ff',      # broadcast
              '00:00:00:00:00:00',      # broadcast
              '33:33:00:',              # ipv6 multicast
              '33:33:ff:',              # spanning tree
              '01:80:c2:00:00:00',      # multicast
              '01:00:5e:',              # broadcast
              mon_MAC]

    for i in ignore:
        if i in addr1 or i in addr2:
            return True


########################################
# End output filtering
########################################





########################################
# Set packet handling 
########################################

def cb(pkt):
    '''
    Look for dot11 packets that aren't to or from broadcast address,
    are type 1 or 2 (control, data), and append the addr1 and addr2
    to the list of clients
    '''
    global clients_APs, APs

    # We're adding the AP and channel to the clients list at time of creation rather
    # than updating on the fly in order to avoid costly for loops that require a lock
    if pkt.haslayer(Dot11):
        if pkt.addr1 and pkt.addr2:
            pkt.addr1 = pkt.addr1.lower()
            pkt.addr2 = pkt.addr2.lower()

            # Filter out all other APs and clients if asked
            if args.accesspoint:
                if args.accesspoint not in [pkt.addr1, pkt.addr2]:
                    return

            # Check if it's added to our AP list
            if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                APs_add(clients_APs, APs, pkt, args.channel, args.world)

            # Ignore all the noisy packets like spanning tree

            if noise_filter(pkt.addr1, pkt.addr2):
                return

            # Management = 1, data = 2
            if pkt.type in [1, 2]:
                clients_APs_add(clients_APs, pkt.addr1, pkt.addr2)


def APs_add(clients_APs, APs, pkt, chan_arg, world_arg):
    ssid       = pkt[Dot11Elt].info
    bssid      = pkt[Dot11].addr3.lower()
    try:
        # Thanks to airoscapy for below
        ap_channel = str(ord(pkt[Dot11Elt:3].info))
        chans = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'] if not args.world else ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'] 
        if ap_channel not in chans:
            return

        if chan_arg:
            if ap_channel != chan_arg:
                return

    except Exception as e:
        return


    # ----------------------------------------------
    # This is the money shot.
    # We have an observation of a bssid, ap_channel, and ssid,
    #  plus we have the raw packet so we can get
    #  a timestamp too. 
    # Next step is modify this code and add it to a DB.
    data = { 'bssid' : bssid,
             'channel' : ap_channel,
             'ssid' : ssid
             }

    print data

    ### if len(APs) == 0:
    ###     with lock:
    ###         return APs.append([bssid, ap_channel, ssid])
    ### else:
    ###     for b in APs:
    ###         if bssid in b[0]:
    ###             return
    ###     with lock:
    ###         return APs.append([bssid, ap_channel, ssid])

    # ----------------------------------------------




def clients_APs_add(clients_APs, addr1, addr2):

    # ----------------------------------------------
    # This is the money shot.
    # We have an observation of a client, addr1, addr2, channel, mac
    #  plus we have the raw packet so we can get
    #  a timestamp too. 
    # Next step is modify this code and add it to a DB.

    data = {'client' : addr1,
            'station' : addr2,
            'channel' : monchannel
            }

    print data

    ### if len(clients_APs) == 0:
    ###     with lock:
    ###         return clients_APs.append([addr1, addr2, monchannel])

    ### # Append new clients/APs if they're not in the list
    ### else:
    ###     for ca in clients_APs:
    ###         if addr1 in ca and addr2 in ca:
    ###             return

    ###     with lock:
    ###         return clients_APs.append([addr1, addr2, monchannel])

    # ----------------------------------------------




########################################
# End packet handling 
########################################


def stop(signal, frame):
    if monitor_on:
        sys.exit('\n['+R+'!'+W+'] Closing')
    else:
        remove_mon_iface(mon_iface)
        os.system('service network-manager restart')
        sys.exit('\n['+R+'!'+W+'] Closing')

if __name__ == "__main__":
    if os.geteuid():
        sys.exit('['+R+'-'+W+'] Please run as root')
    clients_APs = []
    APs = []
    DN = open(os.devnull, 'w')
    lock = Lock()
    args = parse_args()
    monitor_on = None
    mon_iface = get_mon_iface(args)
    conf.iface = mon_iface
    mon_MAC = mon_mac(mon_iface)
    first_pass = 1

    # Start channel hopping
    hop = Thread(target=channel_hop, args=(mon_iface, args))
    hop.daemon = True
    hop.start()

    signal(SIGINT, stop)

    print "sniffing"
    sniff(iface=mon_iface, store=0, prn=cb)

