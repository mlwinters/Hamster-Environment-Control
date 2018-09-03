# Hamster Environment Control

This repository contains the Python files for my Hamster Environment Control system.<br/>
The readme contains important info about the system and should be read carefully before installing or executing.<br/>


## Description

Hamster Environment Control refers to the software package that runs on my .Ux project.<br/>
The .Ux is a hamster cage with an integrated Raspberry Pi computer that currently serves 4 main function:<br/>

1. Controls the automatic cage lighting to switch either the white or red lights on/off depending the time of day. It also switch the infrared cage lights on during the night but only if the camera is running.<br/>
2. Monitors the temperature of the cage and reports when the temperature is outside of a given range.<br/>
3. Controls the cage camera and either streams the camera data over a local network or records the data to a h264 video file to be viewed/edited later.<br/>
4. HEC also logs system events to a text file, logs the cage temperature every 30 mintues as well as serveral other less important tasks.<br/>
(See System Details below for more info)<br/><br/>

Although HEC was written for a hamster cage, it could be used for any small animal cage such as gerbils, mice, rats, chinchillas or degus.<br/>


## Important Notes

This software was written to run on a Raspberry Pi 1 (first release) running Raspbian Wheezy Version 2013-09-10 and Python 2.7.
You may need to edit some or all script files if you using a newer RPi 2/3 ect, a newer version of Raspbian, Python 3.x or a completely different operating system like Ubuntu or RISC OS.<br/>

It is assumed that you have a basic knowledge of Linux, Python and that you are running a fresh install of Raspbian.<br/>

This system uses the RPi GPIO library, Adafruit BME280 Python library and others which are NOT inclued in this repository. See "Installation" below to find out how to download and install all the required libraries.<br/>

Although HEC.py, cc-stream and cc-record need the Adafruit BME280 sensor board and its driver to function. I have released "-no-sensor" versions of the camera software incase you wish to use the code for a different type of project such as a dash-cam or robot/rover.<br/> 

It is recommended that you connect your RPi to your home network to allow you control your RPi via a SSH connection, view network camera, log files ect.<br/>
Internet connection is required for installation and the RPi will also try to acquire the time/date during system boot. Unless you have a third party Real Time Clock module, you should keep your RPi connected to the internet so that it keeps an accurate time.<br/>
HEC.py or any of the camera programs do not need the internet themselves but do require the time/date.<br/>

Before running any of the scripts in this repository, you will need to check hec-config.ini and change it to suit your needs.<br/>
You will also need to update the GPIO pin numbers inside HEC.py as well. I have made it clear inside these files what you need to edit. Search "#####" for the lines you may need to edit.<br/>

Please note that I will not provide support or help with installation or the operation of HEC. I will update this software and fix bugs when needed but I will not update it for your needs or for new releases of the Raspberry Pi, Raspbian, Python 3.x ect. It is up to you to modify to the code for your setup.<br/>
Any issues with third party libraries should be raised with their respective authors.<br/><br/>


## Requirements

Hardware:<br/>
(Core requirments)<br/>
Raspberry Pi 1 Model B (512Mb RAM),<br/>
Minimum of 8Gb SD Card (32Gb recommended),<br/>
5V DC power supply with minimum of 1.0A output current (just for RPi) (2.5Amp for newer RPi 2/3 and fitted with a fast blow fuse),<br/>
Seperate 15V DC power supply with minimum of 1.0A output current (for rest of electronics) (with a fast blow fuse),<br/>
Raspberry Pi Camera (Version 2, 8MP),<br/>
Adafruit BME280 temperature sensor,<br/>
Local network connection (for viewing network camera, log files ect),<br/>
Internet connection (for installation and at system startup to time/date unless you have a RTC),<br/>

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
VLC<br/>
 

## Installation

From a fresh install of Raspbian, boot up your RPi and log in, then do the following:<br/>
Step 1 (Setting up RPi) Expanding Filesystem, enabling I2C and Camera;<br/>
a) From the terminal, type the following and then use the up/down arrow keys to select "Expand Filesystem".
```
sudo raspi-config
```
Once done, Raspi-config will return to the main screen.<br/>

b) Select "Enable Camera", you'll be asked whether to enable support for RPi camera, Select "Yes".<br/>
Raspi-config will then return to the main screen.<br/>

c) Select "Advanced Options" and select I2C then "Yes".<br/>
You'll then be asked whether to enable I2C kernal module, Select "Yes".<br/>
(if your only going to use the "-no-sensor" versions of the camera software, you can skip this step)<br/>
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

b) Once they have all downloaded, go to the following address to download the Adafruit GPIO library:<br/>
https://github.com/adafruit/Adafruit_Python_GPIO<br/>
and follow the instructions as outlined in the README file.
(if your only going to use the "-no-sensor" versions of the camera software, you can skip this step)<br/>

c) When the Adafruit GPIO library has been downloaded, go to the following address to download the Adafruit BME280 library:<br/>
https://github.com/adafruit/Adafruit_Python_BME280<br/>
and follow the instructions as outlined in the README file.<br/>
(if your only going to use the "-no-sensor" versions of the camera software, you can skip this step)<br/>

d) Next you need to download the PiCamera library, go to:<br/>
https://picamera.readthedocs.io/en/release-1.13/install.html<br/>
and follow the installation instructions on that page.<br/><br/>


Step 4 (Downloading Hamster Environment Control)<br/>
Once everything else has been installed, you can then download Hamster Environment Control.<br/>
a) To clone this repository type the following
```
cd
sudo git clone https://github.com/mlwinters/Hamster-Environment-Control
```

b) Once HEC has downloaded, run the following command to run the setup file,
```
sudo python Hamster-Environment-Control/HEC-Setup.py
```
This will create two folder inside the Hamster Environment Control folder for the log files and videos. It also sets the file permissions of hec-status.ini to 007 to allow cc-stream.py to read/write to it.<br/><br/>


## Configuration

I have septerated out most of the user definable settings to hec-config.ini where you'll find the climate control, lighting and thread update speed settings.<br/><br/>
The values in the climate section are the minimum, normal and maximum temperatures and are in degrees celsius. If you change these, make sure you keep the .10 buffer to prevent the log file from getting spammed if the temperature hovers around two values.<br/><br/>
Values in the lighting section are the times which the cage lighting is switched. Using a 24 hour clock.<br/><br/>
Values in the thread section are the update speed of each of the system's background threads. Values are in whole seconds.<br/><br/>
The log file section should only be changed if you really need to change it. Only change the "/Hamster-Environment-Control/" part, do not change any other part or the log files will not be created.<br/><br/>
The systemreboottime value in housekeeping is self explanatory. When the system time is that value, it triggers a system restart. The pre-set time of just before midnight ensures that the last log entry has the correct time/date and that when the RasPi has finshed restarting the new log file has correct time/date.<br/>

It is best to make a back-up copy of this file when editing any files incase your changes don't work.<br/>
Note that the hec-status.ini is NOT a user configuration file. It is used by HEC.py and the camera software for the text overlay in the stream/video. Please don't fiddle with it.<br/>


## Execution

As HEC was designed to be running 24/7 and because the system restarts once a day, you will need Raspbian to run HEC.py after startup.<br/>
There are serveral ways of doing this, I have done the following
```
sudo nano /etc/rc.local
```
Go all the way down untill you find "exit()" and insert a new line above with the following
```
sudo python /home/pi/Hamster-Environment-Control/HEC.py
```

Then press Ctrl+X to save the changes, HEC will then run on startup. To stop this, type
```
sudo nano /etc/rc.local
```

Again and either remove the line your added previously or simply insert a "#" infront of it, save it and restart your RPi.<br/>


Just to start Hamster Environment Control while the RPi is running, simply type the following
```
sudo python /home/pi/Hamster-Environment-Control/HEC.py
```

To stream camera data over a local network, type the following
```
python /home/pi/Hamster-Environment-Control/Camera/cc-stream.py
```

To record camera data to a video file, type the following
```
sudo python /home/pi/Hamster-Environment-Control/Camera/cc-record.py
```

cc-record.py will ask you to specify a the length for the video, type in a value in whole minutes.<br/>
cc-record.py will also ask you if you want the text annotation to be overlayed on the video.<br/>
Once the recording has started, your video file will be saved to:<br/>
/home/pi/Hamster-Environment-Control/Videos/<br/>

And will have the time and date (as it was when the recording started) as the filename.<br/>
Don't use run cc-stream.py as a root user, VLC doesn't like it and the stream won't be started.<br/><br/>

When using cc-stream.py or cc-stream-no-sensor.py, you will need a media player that supports network streams. I recommend using VLC which is available Windows, macOS, Linux, Android and iOS and others. To access the stream, select "Open Network Stream" in the "Media" menu, then type the following into the "Please enter a network URL:" box,
```
rtsp://<ip_address>:8554/
```
Replace the "<ip_address>" with the IP adress of your Raspberry Pi, for example rtsp://192.168.0.102:8554/<br/>
Please note that cc-stream.py and cc-stream-no-sensor.py do tend to have a couple second delay due to the vlc buffering process. This buffer can sometimes trigger a slight freeze in the stream the lasts for about 1 second, however the stream itself is very stable over many hours.<br/><br/>

## System Details:

Automatic Cage Lighting;<br/>
White cage lights are enabled between 0900 and 1800 automatically.<br/>
Red cage lights are enabled between 1800 and 0000 automatically.<br/>
Infrared cage lights are enabled between 0000 and 0900 automatically but only if the camera is running (either recording or streaming).<br/>

Climate Control;<br/>
Temperature is read once a second and writes an entry to the log file if the cage temperature reaches the either the minimum, normal or maximum temperatures. The system fan is also enabled when temperature is too high to reduce the risk of the power supply from overheating.<br/>

Event Logging;<br/>
This logs system events to a text file for review at a later time/date. System will create a new log file every 24 hours (at midnight) and a new folder inside /HEC-Logs every week (sunday/monday midnight).<br/>
Cage temperature is also recorded to this log file every 30 minutes.<br/>

Network Camera / Video Recorder;<br/>
cc-stream.py pipes camera data over a local network so you can monitor your pet remotely without disturbing them.<br/>
cc-record.py saves camera data to a h264 video file for viewing and editing later. Unless your video player/editing software supports .h264 files. Videos will need to be converted into a MP4 file which can be done with such programs as MP4Box.<br/>
Both cc-stream and cc-record use the same camera settings and both reply on hec-status.ini to function.<br/>
I have also included the "-no-sensor" versions of cc-stream.py and cc-record.py. These are the same as the normal versions but without support for the Adafruit BME280 temperature sensor incase you do not have it.<br/>
The camera is not controlled by the main Hamster Environment Control program but the automatic infrared lighting is controlled by HEC.py.<br/><br/>


## License

Hamster Environment Control free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.<br/>

Hamster Environment Control is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.<br/><

You should have received a copy of the GNU General Public License along with Hamster Environment Control.  If not, see <http://www.gnu.org/licenses/>.<br/>

This software contains code written by Adafruit Industires. These sections of code where taken from the example included with the BME280 library which was released under the MIT license and can be found here: https://github.com/adafruit/Adafruit_Python_BME280 <br/>

This software contains code written by Dave Jones. These sections of code where taken from the examples included on the PiCamera website which was released under the GNU General Public License Version 2 and can be found here: https://picamera.readthedocs.io/en/release-1.13/<br/>


## Copyright

Copyright (C) 2018 Morgan Winters <morgan.l.winters@gmail.com><br/><br/>


## Special Thanks

Adafruit Industries, Dave Jones <dave@waveform.org.uk><br/><br/>


## Community Contributions

Being an open source project, I welcome people contributing to this software but please note that any changes will be fully tested over a few days or weeks to ensure stability. Thus changes or Commits to this repo will not happen straight away. Also, some contributions may not be used for one reason or another, I will do my best to explain why I haven't included your contribution. Please don't be offended if I don't use your code.<br/>

This software is released under the GNU GPL V3, therefore your code contributions must be supplied under the same license.<br/>

As stated in the License section, you can download, execute, modify and redistribute this work under the terms of the GNU GPL Version 3.<br/><br/>


## Misc

I have specified the Raspberry Pi version/model and operating system version due to the fact that I have not tested these programs on any later version of the Raspberry Pi, Raspbian or with Python 3.x.<br/>
Therefore I cannot judge the software's compatibility or stability with newer versions of the Raspberry Pi like the Pi2, Pi3 ect, Raspbian or Python 3.x.<br/>

If you are using any newer versions of the Raspberry Pi, RasPi Camera, Raspbian or Python it is up to you to get it working for your setup. I cannot test this software on every single hardware configuration possible.<br/>

Although this is NOT a requirement, I would appreciate it if anyone who redistributes versions of Hamster Environment Control or the camera software could send me a quick email with a link to your project. Again contacting me is NOT required and is completely optional.<br/>

