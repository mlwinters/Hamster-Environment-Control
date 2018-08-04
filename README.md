# Hamster Environment Control

Thanks for dropping by, I am currently preparing and running finals tests on the initial alpha version of HEC as well as writting the full readme file. I will be releasing the rest of the software over the next week or two so please bear with me and check back soon.

## Description

Hamster Environment Control refers to the software package that runs on my .Ux project. The .Ux is a Raspberry Pi controlled hamster cage that serves 3 main function:<br/>
1) Controls the automatic lighting in the cage and switches either the white or red cages lights depending on the time of day. It will also switch the infrared cage lights on between certain times but only if the camera is running.<br/>
2) Monitors the temperature of the cage and reports when the temperature is outside of a given range. <br/>
3) Controls the cage camera and either streams the camera data over a local network or records the data to a h264 video file to be viewed/edited later.<br/>
The system also logs events to a text file, logs the cage temperature every 30 mintues to this text file as well as serveral other less important tasks.<br/><br/>
 

So far I have only released part of the software. The Camera folder contains two Python files used for the Raspberry Pi camera module.</br>
cc-stream.py captures data from the Raspberry Pi camera module and pipes it to VLC to be live streamed over a local network.<br/>
cc-record.py records video data and saves it to a h264 file for viewing or editing at a later time.<br/>
I have included a README file in the Camera Folder with more details and installation instructions.<br/><br/>


Please Note: Apart from a Raspberry Pi camera module, you also need the Adafruit Industries BME280 temperature sensor alone with it's Python library. Other libraries/software are required for the cc-stream.py and cc-record.py to run. See the README within the Camera folder.<br/>


## Installation

If you haven't downloaded the required libraries, please see the README file in the Camera folder for a detailed step-by-step on how to get the camera up and running.

Once you have the Adafruit BME280 sensor board and have downloaded all of the required libraries and software you can then download this repository to your Raspberry Pi, simply type the following commands into the terminal:
```
cd
git clone https://github.com/mlwinters/Hamster-Environment-Control.git
sudo mkdir /home/pi/Hamster-Environment-Control/Videos
```
<br/>


## Execution

To run the camera software type one of the following:<br/>
To start the live stream type;
```
python /home/pi/Hamster-Environment-Control/Camera/cc-stream.py
```
To start the video recorder type;
```
python /home/pi/Hamster-Environment-Control/Camera/cc-record.py
```

## Contributions

I welcome people contributing and making Pull Requests but please note that any changes will be fully tested over a few days or weeks to ensure stability. Thus changes or Commits to this repo will not happen straight away. Also, some contributions may not be used for one reason or another, I will do my best to explain why I haven't included your contribution. Please don't be offended if I don't use your code.<br/><br/>

The software is released under the GNU GPL V3, your code contributions must be supplied under the same license.
