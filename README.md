# wifi-data

Welcome to the repository for the Internet of Things Wireless Network Data project. 
This project is part of an undergraduate research project at South Seattle College, Winter Quarter 2016.



## Project Overview

This project is intended to get students involved in research by designing and assembling a distributed
sensor network that consists of embedded microcomputers generating data and sending out the data on a pipeline
to a centralized database, where the data can be analyzed.

In our particular project, the distributed sensors are Raspberry Pi microcomputers. The Raspberry Pis have on-board
wireless cards that are listening to nearby wireless traffic and creating a profile of wireless activity.
This gives us a time-evolving snapshot of wireless network traffic in a given location. 

Our project relates to the broader concept of the Internet of Things because, as computer hardware becomes smaller and smaller, 
the line between the digital and physical world is blurring, and embedded sensors that generate streams of data are constantly
becoming cheaper and smaller. 



## Code Overview

This Github repository contains code for each component of the data pipeline, plus some additional illustrative examples. 

The Raspberry Pis are collecting wireless data using the aircrack suite (specifically, the `airodump-ng` utility), 
which is being run by a Python script. The resulting data about wireless traffic is in CSV format and consists of 
observations about unique devices and access points that are transmitting wireless traffic.

These CSV files are then transferred to a central server and processed with a Python script to extract individual 
observations and push them into a central SQL database.  This SQL database is a SQLite database.

Finally, there are scripts to analyze the data. These scripts calculate derived quantities from the raw, observed data. 
These derived quantities can either be calculated anew each time the script is run, or they can be calculated and 
stored back in the database as a derived quantity. This creates a quantitiative, data-driven picture of the network.



## Code Specifics: In The Repository

The breakdown of tasks needed to implement a data pipeline for a distributed sensor network boils down to:

1. Scripts to collect wifi data onboard the sensors

2. Scripts to process CSV files into SQL records

3. Scripts to extract, analyze, and crunch data

Each task corresponds to a directory: 

* `pi/` - scripts for capturing wireless data with the Raspberry Pi

* `process_csv/` - scripts for processing CSV files to turn them into SQL records

* `analysis/` - scripts for mathematical analysis of wifi data, extracted from SQL database

Some additional code is located in:

* `pywifi/` - scripts for doing wifi stuff with Python

* `datetime/` - explanatory code for dealign with dates and times in Python






