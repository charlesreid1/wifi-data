# Internet of Things Wireless Sensor Data Project

Welcome to the repository for the Internet of Things Wireless Network Data project. 
This project is part of an undergraduate research project at South Seattle College.

## Project Overview

In this project, we will be operating an internet of things sensor.
Specifically, this will be a Raspberry Pi with a directional Wifi antenna.
The Raspberry Pi will collect wifi signal data.

This data will be collected on a server, and processed and analyzed.
As part of the proejct we will be looking at the time-evolving picture
of wireless network traffic in a given location.

## Task Overview

The task of implementing an internet of things thing to collect and process
wifi data can be broken down into the following subtasks: 
* (Future work) Control an antenna rotator 
* Control the wifi antennas (monitor mode, join networks, etc.)
* Collect wifi data onboard the thing
* Copy data to a command and control (C2) server
* Process the resulting data

## Directories

Scripts related to each individual task are in folders:
* `antenna/` - scripts for controlling the antenna mode and antenna rotator 
* `collect/` - scripts for collecting data from the wifi interface
* `exfiltrate/` - scripts for exfiltrating data to a command and control server
* `processing/` - scripts for processing resulting wifi data

