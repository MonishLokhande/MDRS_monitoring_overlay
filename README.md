# MDRS_monitoring_overlay
Purdue MDRS crew 288 and 289 raspberry pi hosted remote station monitoring system.

This repo should contain schematics as well as docs and software used for the project for easy access for entire crew
  - While MDRS crews are on site sim should be maintained by respecting the ~22 minute lag time between mission control updates and pulling anything from the repo

## Sensor Values
Reading from 5 air quality sensors (with datasheets)
 - temp / humidity (combined in one sensor)
   - http://aosong.com/userfiles/files/media/Data%20Sheet%20AHT21.pdfhttp://aosong.com/userfiles/files/media/Data%20Sheet%20AHT21.pdf 
 - CO2
   - https://cdn-reichelt.de/documents/datenblatt/C150/MH-Z19C-PC_DATENBLATT.pdf
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

## Setup
Install Thonny [https://thonny.org]
  - Not the best code editor but flashes data to pi pico very easily

Download pico firmware at [https://rpf.io/pico-w-firmware](https://rpf.io/pico-w-firmware)

Running Code (Instructions mainly from https://projects.raspberrypi.org/en/projects/get-started-pico-w/1)
  1. Clone git directory
  2. Connect pico to computer via micro usb
  3. Place firmware file into pico drive folder (You can literally just drag it)

     - pico folder in your file explorer should disappear
  
  5. Bottom right corner of Thonny shows what editor is being used, you should be able to select  ‘MicroPython (Raspberry Pi Pico)’ 
  6. Use save as in Thonny to save necessary code onto pico
    - main.py always runs on pico boot

accessory files
  - When you add your code to the pico make sure to also add
      - securityInfo.py
      - txtLog.html
  - txtLog.html is the website that will be displayed on the server and is in the repo
  - securityInfo.py is a 4 line file ignored by git you'll create yourself, it's what allows the pico to connect to the local wifi and provides security to the website we'll be hosting. The file should only contain the following three lines

      ssid = "wifi name"
    
      wifi_password = "wifi password"

      website_password = "website_password"
    
#### Local Sensor Log Setup

CollectSensorData.py is a function that calls the read"X".py values in the repo above every hour and saves them into a timestamped txt file. It does not host any website or send that file anywhere. However, it can be used for sensor testing during code development and as a minimum way to log timestamped environmental data.

A few notes
- There isn't much memory on the pico boards, I'll need to do some testing to see how long this setup works before we run into memory issues
- This doesn't use the pico's low power mode (yet) so power consumption will be higher, perhaps lasting only a few days of constant use instead of the two weeks expected with better power management 

Setup instructions
1. To set it up simply save the file onto the pico board
2. Rename it to main.py so that it runs on startup.
3. Copy the read"X".py files from the github, currently makes calls to following
    - readCO2
    - readOnboardTemp
    - readPM2_5
    - readVOC
4. To collect sensor data connect back to the pi via micro usb and download the sensor lof txt files onto your machine


#### Port Forwarding
TODO

Necessary step to making remotely available, will add instructions here at later date

## Website Features and GUI format
At minimum, website shows log of sensor data that can then be downloaded remotely by mission support for backup storage
  - Should also contain GUI to format overlay and make data easily readable
  - Other web pages and general layout TODO
    
Server must be passoword protected so that data is not publically available
  - TODO
