# Raspberry Pi 

## Wifi Data Startup Script

This folder contains two files of interest:

`capture-wifi-data` - this is a startup script that goes into
the `/etc/init.d/` folder on the Raspberry Pi.

Don't forge to make it executable and add it to startup services!

`capture_wifi_data.py` - this is a Python script that puts
the wireless card into monitor mode, then collects wifi 
data with airodump for two hours.

This script should be put into a new directory at
`/root/wifi_data/`, and all csv files will be put in that
directory.

