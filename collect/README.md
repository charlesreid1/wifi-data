# Collect

This directory contains scripts for collecting data from the wifi interface. 
These scripts primarily rely on aircrack and its built-in wifi parsing
capabilities, but this can also be done with Scapy or another specialized
tool. Aircrack is simply the easiest route.

## Aircrack

Script `AircrackIntervals.py`:
* A script to collect data from the interface. 
* New files are created at specified time intervals.
* Total number of files collected is specified. 

## Scapy

Airoscapy is an aircrack-style clone for scanning nearby wifi networks
and clients, written using Python's Scapy library. This allows more 
flexibility in customizing how the packets are read, what particular 
information is kept, and how the information is ultimately used.



