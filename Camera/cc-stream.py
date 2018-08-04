### Copyright ###
# Cage Camera Stream
# Version: 0.1.1 Alpha
# Author: Morgan Winters
# Created: 18/03/2018
# Copyright (C) 2018 Morgan Winters
#
# This file is part of Hamster Environment Control.
#
# Cage Camera Stream is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Cage Camera Stream is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cage Camera Stream.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This software contains code written by Adafruit Industires. These sections of code 
# where taken from the example included with the BME280 library which was released under
# the MIT license and can be found here: 
# https://github.com/adafruit/Adafruit_Python_BME280
###

### Description ###
# Cage Camera Stream uses the PiCamera Python library to stream a data from the Raspberry Pi Camera Module and pipes it to VLC to 
# be streamed over a local network. PiCamera allows for greater flexibility than just using the raspivid command. It allows
# for the text annotation to be refreshed and changed without stopping the recording. This program displays the time and date,
# white, red and infrared cage light status as well as sensor data from the Adafruit BME280 temperature sensor and updates
# the text annotation once a second for the duration of the stream.
# This program also uses the VLC library to stream camera data over a local network. VLC media player is then used to view the
# stream from a client desktop/laptop/mobile device by entering "rtsp://<raspi ip address>:8554/" in "Open Network Stream".
# PiCamera, VLC and the Adafruit BME280 libraries all need to be installed on your RasPi for this software to run.
###



### IMPORTS ###
import ConfigParser, shlex, subprocess 
import datetime as dt
from time import sleep
from Adafruit_BME280 import *
import picamera
###

### SETUP ###
# Config Setup #
try:
   ConfigFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"
   Config = ConfigParser.ConfigParser()
   Config.read(ConfigFile)
except:
  print("Unable to load " + ConfigFile + ".")
  print("Please make sure it is present and not corrupted and try again.")
  print("")
  print("Cage Camera Stream will now exit")
  sleep(2)
  exit()


## Sensor Setup ##
try:
  # This section was written by Adafruit Indusdstries and was taken from the #
  # example file included with the Adafruit BME280 library: #
  # https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280_Example.py #
  sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
  # End of Adafruit code #
except:
  print("Unable to load the Adafruit BME280 library.")
  print("If you have installed it, please run the example file included with the library to ensure it's working.")
  print("Otherwise, please go to the following website to download it:")
  print("https://github.com/adafruit/Adafruit_Python_BME280/blob/master/")
  print("")
  print("Cage Camera Stream will now exit")
  sleep(2)
  exit()
##

## Variables ##
## Static Variables ##
# Version #
Version = "0.1.1 Alpha"
#

# Pet Name #
PetName = "Tux"
#

# Text Annotation #
AnnotationUpdateSpeed = 1

# Camera #
Camera = picamera.PiCamera()
VlcCommand = "cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264"
#
##

## Non-Static Variables ##
# Sensor Readings #
CurrentTemp = "00.00"
CurrentHumidity = "00.00"
CurrentMBar = "0000.00"
CurrentPSI = "00.00"
#

# Status #
# Camera #
RecordingStatus = False
#
##
###


### Functions ###
## System ##
# Get System Date/Time/Day #
def GetTime():
  timeNow = dt.datetime.now()
  time = timeNow.strftime("%H:%M:%S")
  return (time)

def GetDate():
  dateNow = dt.datetime.now()
  date = dateNow.strftime("%d-%m-%Y")
  return (date)

def GetDay():
  dayNow =  dt.datetime.now()
  day = dayNow.strftime("%a")
  return (day)
#

# Update Log File #
def UpdateConfigFile(_section, _parameter, _value):
  Config.set(_section, _parameter, _value)
  with open(ConfigFile, 'wb') as cfg:
    Config.write(cfg)
#

## I2C ##
def ReadSensor():
  global CurrentTemp
  global CurrentHumidity
  global CurrentMBar
  global CurrentPSI
  try:
    # This section was written by Adafruit Industries and was copied and then modified from the #
    # example file included with the Adafruit BME280 library: #
    # https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280_Example.py #
    temp = sensor.read_temperature()
    humidity = sensor.read_humidity()
    pascals = sensor.read_pressure()
    mbar = pascals / 100 + 12 # the plus 12 is a rough altitude compensation
    psi = mbar * 0.0145037738
    CurrentTemp = format(temp, ".2f")
    CurrentHumidity = format(humidity, ".2f")
    CurrentMBar = format(mbar, ".2f")
    CurrentPSI = format(psi, ".2f")
    # End of Adafruit code #
  except:
    print("Unable to read temperature sensor.")
#

# Puts Sensor Readings Into A String 
def GetSensorReading():
  global CurrentTemp
  global CurrentHumidity
  global CurrentMBar
  global CurrentPSI
  try:
    ReadSensor()
    SensorReadingString = "Temperature; " + CurrentTemp + "C | Relative Humidity; " + CurrentHumidity + \
                          "% | Pressure; " + CurrentMBar + "mB - " + CurrentPSI + "psi"
    return (SensorReadingString)
  except:
    print("Unable to read temperature sensor.") 
    return ("Unable to read temperature sensor.")
#
##

## Camera ##
# Stream Camera
def StreamCamera():
  global RecordingStatus
  global AnnotationUpdateSpeed
  print("Setting up camera...")
  # Set camera capture options
  Camera.resolution = (1280, 960)
  Camera.framerate = 25
  Camera.exposure_mode = "night"
  Camera.sharpness  = 100
  Camera.brightness = 62
  Camera.awb_mode = "tungsten"
  Camera.ISO = 800
  Camera.hflip = True
  Camera.vflip = False
  Camera.annotate_background = True
  Camera.annotate_text_size = 20
  RecordingStatus = True
  UpdateConfigFile('status', 'camera', "True")
  cvlc = subprocess.Popen(shlex.split(VlcCommand), stdin=subprocess.PIPE)
  print("Starting VLC...")
  Camera.start_recording(cvlc.stdin, format='h264')

  while RecordingStatus:
    try:
      # Get HEC system status from HEC status file
      Config.read(ConfigFile)
      whitelightstatus = Config.get('status', 'whitelights')
      redlightstatus = Config.get('status', 'redlights')
      irlightstatus = Config.get('status', 'infraredlights')
      climatecontrolstatus = Config.get('status', 'climatecontrol')
      # Overlay text to stream
      Camera.annotate_text = PetName + " Cage-Cam\n\nTime; " + GetTime() + " (BST) | Date; " + \
                             GetDay() + " " + GetDate() + "\nWhite Lights; " + whitelightstatus + \
                             " | Red Lights; " + redlightstatus + " | Infrared Lights; " + irlightstatus + \
                             " | Climate Control; " + climatecontrolstatus + "\n" + GetSensorReading()
      sleep(AnnotationUpdateSpeed)
    except KeyboardInterrupt:
      print("cc-stream stopped.")
      UpdateConfigFile('status', 'camera', "False")
      raise
    except:
      print ("Unable to overlay text.")
  else:
    pass
##
###

### Execute ###
## Camera ##
StreamCamera()
##
###