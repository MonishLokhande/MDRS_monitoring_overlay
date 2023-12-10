# MDRS_monitoring_overlay
Purdue MDRS crew 288 and 289 raspberry pi hosted remote station monitoring system.

This repo should contain schematics as well as docs and software used for the project for easy access for entire crew
  - While MDRS crews are on site sim should be maintained by respecting the ~22 minute lag time between mission control updates and pulling anything from the repo

## Sensor Values
Reading from 5 air quality sensors (with datasheets)
 - temp / humidity (combinewd in one sensor)
   - http://aosong.com/userfiles/files/media/Data%20Sheet%20AHT21.pdf 
 - CO2
   - https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19c-pins-type-co2-manual-ver1_0.pdf
 - PM2.5
   - https://wiki.keyestudio.com/Ks0196_keyestudio_PM2.5_Shield
 - VOC
   - https://www.winsen-sensor.com/d/files/zp07-mp503-10-grade-manual-air-quality-detection-module-1_3-terminal-forward.pdf
 - Ozone
   - https://cdn.sparkfun.com/assets/9/9/6/e/4/mq131-datasheet-low.pdf

One pi pico board connected to above 5 air quality sensors for each of the 5 MDRS buildings
 - RAM (Not in place for crew 288)
 - Hab floor 1
 - Hab 2
 - Science Dome
 - Greenhab
   
Measuring airlock status using reed switches and magnets
 - One pi in each of the airlocks to measure these
Measuring EVA suit charge status using GPIO voltage detection

## Website Features and GUI format
Currently planned to be hosted on raspberry pi running nginx server
  - nginx subject to change depending on how the GUI progresses
    
At minimum, website shows log of sensor data that can then be downloaded remotely by mission support for backup storage
  - Should also comprise GUI to format voerlay and make data easily readable
  - Other web pages and general layout TODO
    
Server must be passowrd protected so that data is not publically available
  - TODO
