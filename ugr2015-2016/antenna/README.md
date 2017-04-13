# Antenna

Scripts for controlling the wifi antennas.

## Tasks

There are just two tasks related to the wifi antennas that it is important
we be able to script. 

The first is joining a wireless network. We'll want to be able to look for 
particular trusted wireless networks or open wireless networks, and use 
a USB wifi dongle to connect to those wireless networks. This will allow us
to set up a connection back to the home server.

The second is putting the (directional) wireless antenna into monitor mode.
This is important to do on boot, as the antenna will not start in this mode
by default.

## Joining Wifi Networks

See `JoinWifi.py`

## Wifi Monitor Mode

See `MonitorMode.py`
