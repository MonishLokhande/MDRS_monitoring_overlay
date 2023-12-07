# MDRS_monitoring_overlay
Purdue MDRS crew 288 and 289 raspberry pi hosted remote station monitoring system.

This repo should contain schematics as well as docs and software used for the project for easy access for entire crew
  - While MDRS crews are on site sim should be maintained by respecting the ~22 minute lag time between mission control updates and pulling anything from the repo

## Sensor Values
Reading from x air quality sensors (with datasheets)
 - TODO

One of each of the above sensors in each of the 5 MDRS buildings
 - RAM
 - Hab floor 1
 - Hab 2
 - Science Dome
 - Greenhab
   
Measuring airlock status using reed switches and magnets

Measuring EVA suit charge status using GPIO voltage detection

## Website Features and GUI format
Currently planned to be hosted on raspberry pi running nginx server
  - nginx subject to change depending on how the GUI progresses
    
At minimum, website shows log of sensor data that can then be downloaded remotely by mission support for backup storage
  - Should also comprise GUI to format voerlay and make data easily readable
  - Other web pages and general layout TODO
    
Server must be passowrd protected so that data is not publically available
  - TODO
