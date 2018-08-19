# Cage Camera Stream/Record

Please see the README file inside the main Hamster Environment Control folder for full details.

## Description

These four programs are used for the cage camera on my .Ux project.<br/>
cc-stream.py captures data from the Raspberry Pi camera module and pipes it to VLC to be live streamed over a local network.<br/>
cc-record.py records video data and saves it to a .h264 file for viewing or editing at a later time.<br/>
Both programs require the hec-status.ini file contained in the main Hamster Environment Control folder. <br/>
This file is checked once a second (faster if need) for the text annotation overlay on the stream or video with time/date, cage light status, temperature ect for the duration of the stream/video.<br/>
cc-record.py will ask if you want the text overlay enabled and also asks the user to specify the length of the video before the camera starts.<br/>

I have also included the "-no-sensor" versions of cc-stream.py and cc-record.py. These are the same as the normal versions but without support for the BME280. Use this is you don't have the Adafruit BME280 temperature sensor.<br/>
I wrote this software for the camera in my hamster cage but this code could easily be modified for use as a CCTV camera for wildlife, front doors, baby rooms, dash-cams or even on robotic rovers.<br/>


## Requirements

Hardware:<br/>
Raspberry Pi 1 Model B or later,<br/>
Raspberry Pi Camera Module (Normal or No-IR) Version 2,<br/>
Adafruit Industires BME280 Temperature Sensor,<br/>
Internet connection for installation - Local network and another device for viewing the stream.<br/><br/>

Software:<br/>
Raspbian Wheezy Version 2013-09-10,<br/>
Python 2.7,<br/>
Adafruit Industries Python GPIO library,<br/>
Adafruit Industries BME280 Python library,<br/>
PiCamera library,<br/>
VLC library<br/>


## Installation

Step 1) To download the Adafruit GPIO library, go to https://github.com/adafruit/Adafruit_Python_GPIO
and follow the instructions as outlined in the README file.<br/>
(if your only going to use the "-no-sensor" versions, you can skip this step)<br/>

Step 2) To download the Adafruit BME280 library, go to https://github.com/adafruit/Adafruit_Python_BME280 <br/>
and follow the instructions as outlined in the README file.<br/>
(if your only going to use the "-no-sensor" versions, you can skip this step)<br/>

Step 3) To download the PiCamera library, go to https://picamera.readthedocs.io/en/release-1.13/install.html <br/>
and follow the installation instructions on that page.<br/>

Step 4) To download VLC, type the following commands into the terminal:
```
sudo apt-get update
sudo apt-get install vlc
```
<br/>

Step 5) To download Hamster Environment Control, type the following into the terminal:
```
git clone https://github.com/mlwinters/Hamster-Environment-Control.git
```
<br/>

Step 6) Finally we need to create a folder where cc-record.py will save captured videos to.
Type the follow into the terminal:
```
sudo mkdir /home/pi/Hamster-Environment-Control/Videos
```

## Execution

To stream camera data over a local network, type the following:
```
python /home/pi/Hamster-Environment-Control/Camera/cc-stream.py
```

To record camera data to a video file, type the following:
```
sudo python /home/pi/Hamster-Environment-Control/Camera/cc-record.py
```
cc-record.py will ask you to specify a the length for the video, type in a value in whole minutes.<br/>
cc-record.py will also ask you if you want the text annotation to be overlayed on the video. <br/>
Once the recording has started, your video file will be saved to:
```
/home/pi/Hamster-Environment-Control/Videos/
````
And will have the time and date (as it was when the recording started) as the filename.<br/>


## Copyright

Copyright (C) 2018 Morgan Winters <morgan.l.winters@gmail.com><br/>


## Special Thanks

Adafruit Industries, Dave Jones <dave@waveform.org.uk><br/>
