# Hamster Environment Control

This repository contains the Python files for my Hamster Environment Control system.<br/>
The readme contains important info about the system and should be read carefully before installing or executing.<br/>


## Description

Hamster Environment Control refers to the software package that runs on my .Ux project.<br/>
The .Ux is a Raspberry Pi controlled hamster cage that currently serves 4 main function:<br/>

1. Controls the automatic cage lighting to switch either the white or red lights depending on the time of day.<br/>
It will also switch the infrared cage lights on during the night time but only if the camera is running.<br/>
2. Monitors the temperature of the cage and reports when the temperature is outside of a given range.<br/>
3. Controls the cage camera and either streams the camera data over a local network or records the data to a h264 video file to be viewed/edited later.<br/>
4. The system also logs system events to a text file, logs the cage temperature every 30 mintues as well as serveral other less important tasks.<br/>
(See System Details below for more info)<br/>


## Important Notes
This software was written to run on a Raspberry Pi 1 (first release) running Raspbian Wheezy Version 2013-09-10 and Python 2.7.
You may need to edit some or all script files if you using a newer RPi 2, RPi 3 ect, a newer version of Raspbian, Python 3.x or a completely different operating system like Ubuntu or RISC OS.<br/>

It is assumed that you have a basic knowledge of Linux/Python and that you are running a fresh install of Raspbian.<br/>

This system uses the RPi GPIO library, Adafruit BME280 Python library and others which are NOT inclued in this repository. See "Installation" below to find out how to download and install all the required libraries.<br/>

It is recommended that you connect your RPi to your home network to allow you control your RPi via a SSH connection, view network camera ect.<br/>
Internet connection is required for installation. Linux will also try to acquire the time/date during system boot. Unless you have a Real Time Clock module, you should keep your RPi connected to the internet so that it keeps an accurate time.<br/>
HEC.py nor either of the camera program do not need the internet themselves but do require the time/date.<br/>

Before running any of the scripts in this repository, you will need to check hec-config.ini and change it to suit your needs.<br/>
You will also need to update the GPIO pin numbers inside HEC.py as well. I have made it clear inside these files what you need to edit. Inside HEC.py, search for #####, for the lines you may need to edit.<br/>

Please note that I will not provide support or help with installation or the operation of HEC. I will update this software and fix bugs when needed but I will not update it for your needs or for new releases of the Raspberry Pi or Raspbian.<br/>
Any issues with third party libraries should be raised with their respective authors.<br/><br/>


## Requirements

Hardware:<br/>
(Core requirments)<br/>
Raspberry Pi 1 Model B (512Mb RAM),<br/>
Minimum of 8Gb SD Card (32Gb recommended),<br/>
5V DC power supply with minimum of 1.0A output current (just for RPi)(fused),<br/>
Seperate 15V DC power supply with minimum of 1.0A output current (for rest of electronics)(fused),<br/>
Raspberry Pi Camera (Version 2 (8MP)),<br/>
Adafruit BME280 temperature sensor,<br/>
Local network connection (for viewing network camera),<br/>
Internet connection (for installation and at system startup),<br/>

(Full operation requirments)<br/>
Any 8 channel switch board (ideally using medium power transistors and not relays),<br/>
12V white LED strip for cage lighting (day lights),<br/>
12V red LED strip for cage lighting (evening lights),<br/>
12v infrared LED strip for camera lighting (camera night vision),<br/>

Software:<br/>
Raspbian Wheezy Version 2013-09-10,<br/>
Python 2.7,<br/>
Raspberry Pi GPIO library,<br/>
Adafruit Industries Python GPIO library,<br/>
Adafruit Industries BME280 Python library,<br/>
PiCamera library,<br/>
VLC library<br/>
 

## Installation

From a fresh install of Raspbian, boot up your RPi and log in with the default username and password then do the following:<br/>
Step 1 (Setting up RPi) Expanding Filesystem, enabling I2C and Camera;<br/>
a) From the terminal, type the following and then use the up/down arrow keys to select "Expand Filesystem".
```
sudo raspi-config
```
Once done, Raspi-config will return to the main screen.<br/>

b) Select "Enable Camera", you'll be asked whether to enable support for RPi camera, Select "Yes".<br/>
Raspi-config will then return to the main screen.<br/>

c) Select "Advanced Options" and select I2C and then "Yes".<br/>
You'll then be asked whether to enable I2C kernal module, Select "Yes".<br/>
Raspi-config will then return to the main screen.<br/>

d) If you wish to use a SSH connection to the RPi then select "Advanced Options" again and select "SSH" then select "Enable".<br/>
Raspi-config will then return to the main screen.<br/>

e) Use the left/right arrow keys to select "<Finish>", you'll then be asked to reboot the RPi, select "Yes" and wait for the Pi to restart.<br/><br/>


Step 2 (Update/Upgrade Packages) (internet connection required)<br/>
a) Log back in and type
```
sudo apt-get update
```
This may take a couple of minutes to complete.<br/>

b) Once update is complete, type
```
sudo apt-get upgrade
```
Again this may take a few minutes to complete depending on your internet download speed.<br/>
You may be asked if you want to install certain packages, choose yes to them all.<br/>

c) Once update and upgrade is complete, reboot your RPi by typing in
```
sudo reboot
```
<br/>

Step 3 (Downloading/Installing Required Libraries/Software) (internet connection required)<br/>
a) Once RPi has restarted, login as normal and then type<br/>
```
sudo apt-get install git RPi.GPIO python-pip python-dev python-rpi.gpio vlc
```
If these packages are already installed, apt-get won't try to reinstall them.<br/>

b) To download the Adafruit GPIO library, go to https://github.com/adafruit/Adafruit_Python_GPIO
and follow the instructions as outlined in the README file.<br/>

c) (Downloading/Installing Adafruit BME280 library)
To download the Adafruit BME280 library, go to https://github.com/adafruit/Adafruit_Python_BME280
and follow the instructions as outlined in the README file.<br/>

d) To download the PiCamera library, go to https://picamera.readthedocs.io/en/release-1.13/install.html
and follow the installation instructions on that page.<br/><br/>


Step 4 (Downloading Hamster Environment Control)<br/>
Once everything else has been installed, you can then download Hamster Environment Control.<br/>
a) To clone this repository type the following
```
cd
sudo git clone https://github.com/mlwinters/Hamster-Environment-Control
```

b) Finally we need to create a couple of folders inside the Hamster-Environment-Control folder we just downloaded, one for the system log files the second is where cc-record.py will save video files.
```
sudo mkdir /home/pi/Hamster-Environment-Control/HEC-Logs
sudo mkdir /home/pi/Hamster-Environment-Control/Videos
```
<br/><br/>

## Configuration

I have septerated out most of the user definable settings to hec-config.ini where you'll find the climate control, lighting and thread update speed settings.<br/><br/>
The values in the climate section are the minimum, normal and maximum temperatures and are in degrees celsius. If you change these, make sure you keep the .10 buffer to prevent the log file from getting spammed if the temperature hovers around two values.<br/><br/>
Values in the lighting section are the times which the cage lighting is switched. Using a 24 hour clock.<br/><br/>
Values in the thread section are the update speed of each of the system's background threads. Values are in seconds.<br/><br/>
The log file section should only be changed if you really need to change it. Only change the "/Hamster-Environment-Control/" part, do not change any other part or the log files will not be created.<br/><br/>
The systemreboottime value in housekeeping is self explanatory. When the system time is that value, it triggers a system restart. The pre-set time of just before midnight ensures that the last log entry has the correct time and that when the RasPi has finshed starting back up the new log file has correct date.<br/><br/>

It is best to make a back-up copy of this file when editing it incase your changes don't work.<br/>
Note that the hec-status.ini is NOT a user configuration file. It is used by HEC.py and the camera software for the text overlay in the stream/video. Please don't fiddle with it.<br/><br/>


## Execution

As HEC was designed to be running 24/7 and because the system restarts once a day, you will need Raspbian to run HEC.py on startup.<br/>
There are serveral ways of doing this, I have done the following
```
sudo nano /etc/rc.local
```
Go all the way down until you find "exit()" and insert a new line above with the following
```
sudo python /home/pi/Hamster-Environment-Control/HEC.py
```
Once you saved the changes, HEC will run on startup. To stop this, type
```
sudo nano /etc/rc.local
```
Again and either remove the line your added previously or simply insert a "#" infront of it.<br/>


Just to start Hamster Environment Control while the RPi is running, simply type the following
```
sudo python /home/pi/Hamster-Environment-Control/HEC.py
```


To stream camera data over a local network, type the following:
```
python /home/pi/Hamster-Environment-Control/Camera/cc-stream.py
```
To record camera data to a video file, type the following:
```
python /home/pi/Hamster-Environment-Control/Camera/cc-record.py
```
<br/>
cc-record.py will ask you to specify a the length for the video, type in a value in whole minutes.<br/>
cc-record.py will also ask you if you want the text annotation to be overlayed on the video.<br/>
Once the recording has started, your video file will be saved to:<br/>
/home/pi/Hamster-Environment-Control/Videos/<br/>

And will have the time and date (as it was when the recording started) as the filename.<br/>
Don't use run the camera code as a root user.<br/>


## System Details:

Climate Control;<br/>
Temperature is read once a second and writes a entry to the log file if the cage temperature reaches the either the minimum, normal or maximum temperatures. The system fan is also enabled when temperature is too high to reduce the risk of the power supply from overheating.<br/>

Automatic Cage Lighting;<br/>
White cage lights are enabled between 0900 and 1800 automatically.<br/>
Red cage lights are enabled between 1800 and 0000 automatically.<br/>
Infrared cage lights are enabled between 0000 and 0900 automatically but only if the camera is running (either recording or streaming).<br/>

Event Logging;<br/>
This logs system events to a text file for review at a later time/date. System will create a new log file every 24 hours (at midnight) and a new folder inside /HEC-Logs every week (monday midnight).<br/>
Cage temperature is also recorded to this log file every 30 minutes.<br/>

Network Camera / Video Recorder;<br/>
cc-stream.py pipes camera data over your local network to monitor your pet remotely without disturbing them.<br/>
cc-record.py saves camera data to a h264 video file for viewing and editing later.<br/>
Both cc-stream and cc-record use the same camera settings and both reply on hec-status.ini to function.<br/>
The camera is not controlled by the main Hamster Environment Control program but the automatic infrared lighting is controlled by HEC.py.<br/><br/>



## Contributions

Being an open source project, I welcome people contributing and making Pull Requests but please note that any changes will be fully tested over a few days or weeks to ensure stability. Thus changes or Commits to this repo will not happen straight away. Also, some contributions may not be used for one reason or another, I will do my best to explain why I haven't included your contribution. Please don't be offended if I don't use your code.<br/>

This software is released under the GNU GPL V3, therefore your code contributions must be supplied under the same license.

