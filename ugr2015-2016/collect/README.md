# Collect

This directory contains scripts for collecting data from the wifi interface. 
These scripts primarily rely on aircrack and its built-in wifi parsing
capabilities, but this can also be done with Scapy or another specialized
tool. Aircrack is simply the easiest route.

## MonitorMode.py

Script `MonitorMode.py`:

MonitorMode uses the [Scapy](http://www.secdev.org/projects/scapy/) library 
to access raw packets directly. This is also based on [wifijammer](https://github.com/DanMcInerney/wifijammer) by Dan McInerney.

This currently prints out packet info, but can be modified to filter packets
and process information or statistics to put into a database or etc.

## AircrackIntervals.py

Script `AircrackIntervals.py`:
* A script to collect data from the interface. 
* New files are created at specified time intervals.
* Total number of files collected is specified. 

