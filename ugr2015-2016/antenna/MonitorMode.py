import subprocess

wlan_name = "wlan0"

subprocess.call(["ifconfig",wlan_name,"down"])
subprocess.call(["iwconfig",wlan_name,"mode","monitor"])
subprocess.call(["ifconfig",wlan_name,"up"])

