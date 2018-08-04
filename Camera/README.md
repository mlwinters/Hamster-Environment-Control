# Cage Camera Stream/Record

## Description

These two programs are used for the cage camera on my Hamster Environment Control project. <br/>
cc-stream.py captures data from the Raspberry Pi camera module and pipes it to VLC to be live streamed over a local network. <br/>
cc-record.py records video data and saves it to a .h264 file (see installation below) for viewing or editing at a later time.
Both programs require the hec-status.ini file contained in the main Hamster Environment Control folder. 
This file is checked once a second (faster if need) and will overlay a text annotation on the stream or video with time/date, cage light status, temperature ect for the duration of the stream/video.
cc-record.py will ask if you want the text overlay enabled and also asks the user to specify the length of the video before the camera starts.<br/>
I wrote this software for the camera in my hamster cage but this code could easily be modified for use as a CCTV camera for wildlife, front doors, baby rooms or even on robotic rovers.


## Requirements

Hardware:<br/>
Raspberry Pi 1 Model B or later (see Note A below),<br/>
Raspberry Pi Camera Module (Normal or No-IR) Version 2 (see Note B below),<br/>
Adafruit Industires BME280 Temperature Sensor,<br/>
Internet connection for installation - Local network and another device for viewing the stream.<br/><br/>

Software:<br/>
Raspbian Wheezy Version 2013-09-10 (see Note A Below),<br/>
Python 2.7 (see Note A Below),<br/>
Adafruit Industries BME280 Python library,<br/>
PiCamera library,<br/>
VLC library<br/>


## Installation

Step 1) To download the Adafruit BME280 library, go to https://github.com/adafruit/Adafruit_Python_BME280 <br/>
and follow the instructions as outlined in the README file.<br/>

Step 2) To download the PiCamera library, go to https://picamera.readthedocs.io/en/release-1.13/install.html <br/>
and follow the installation instructions on that page.<br/>

Step 3) To download VLC, type the following commands into the terminal:
```
sudo apt-get update
sudo apt-get install vlc
```
<br/>

Step 4) To download Hamster Environment Control, type the following into the terminal:
```
git clone https://github.com/mlwinters/Hamster-Environment-Control.git
```
<br/>

Step 5) Finally we need to create a folder where cc-record.py will save captured videos to.
Type the follow into the terminal:
```
sudo mkdir /home/pi/Hamster-Environment-Control/Videos
```
<br/>

## Execution

To stream camera data over a local network, type the following:
```
python /home/pi/Hamster-Environment-Control/Camera/cc-stream.py
```

To record camera data to a video file, type the following:
```
python /home/pi/Hamster-Environment-Control/Camera/cc-record.py
```
cc-record.py will ask you to specify a the length for the video, type in a value in whole minutes.<br/>
cc-record.py will also ask you if you want the text annotation to be overlayed on the video. <br/>
Once the recording has started, your video file will be saved to:
```
/home/pi/Hamster-Environment-Control/Videos/
````
And will have the time and date (as it was when the recording started) as the filename.


## Misc

Note A: I have specified the Raspberry Pi version/model and operating system version due to the fact that I have not tested these programs on any later version of the Raspberry Pi, Raspbian or with Python 3.x.<br/>
Therefore I cannot judge the software's compatibility or stability with newer versions of the Raspberry Pi like the Pi2, Pi3 ect, Raspbian or Python 3.x.<br/>

Note B: Again I have specified the camera version as I have the version 2 No-IR camera, I have not tested this software with the version 1 camera.<br/>

If you are using any other versions of the Raspberry Pi, RasPi Camera, Raspbian or Python it is up to you to get it working for your setup. It would be impossible for me to test this software on every single configuration possible.
