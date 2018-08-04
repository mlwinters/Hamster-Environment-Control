### Copyright ###
# Cage Camera Record
# Version: 0.1 Alpha
# Author: Morgan Winters
# Created: 18/03/2018
# Copyright (C) 2018 Morgan Winters
#
# This file is part of Hamster Environment Control.
#
# Cage Camera Record is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Cage Camera Record is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cage Camera Record.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This software contains code written by Adafruit Industires. These sections of code 
# where taken from the example included with the BME280 library which was released under
# the MIT license and can be found here: 
# https://github.com/adafruit/Adafruit_Python_BME280
###

### Description ###
# Cage Camera Record uses the PiCamera library to record data from the Raspberry Pi Camera Module and saves it to h264 video file.
# This allows for greater flexiblty than just using the raspivid command. It allows for the text annotation to be refreshed and 
# changed without stopping the recording. This program displays the time and date, white, red, infrared cage light status as well as
# sensor data from the Adafruit BME280 temperature sensor and updates the text annotation once a second for the duration of the video.
###



### Imports ###
import ConfigParser, os, threading
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
  print("Cage Camera Record will now exit")
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
  print ("Unable to load the Adafruit BME280 library.")
  print ("If you have installed it, please run the example included with the library to ensure it's working.")
  print ("Otherwise, please go to the following website to download it:")
  print ("https://github.com/adafruit/Adafruit_Python_BME280/blob/master/")
  print ("")
  print ("Hamster Environment Control will now exit")
  sleep(2)
  exit()
##

## Variables ##
## Static Variables ##
# Version #
Version = "0.1 Alpha"
#

# Pet Name #
PetName = "Tux"
#

# Text Annotation #
AnnotationUpdateSpeed = 1
#

# Video File #
VideoDirectory = "/home/pi/Hamster-Environment-Control/Videos/"
#

# Camera #
Camera = picamera.PiCamera()
#
##

## Non-Static Variables ##
## Sensor Readings ##
CurrentTemp = "00.00"
CurrentHumidity = "00.00"
CurrentMBar = "0000.00"
CurrentPSI = "00.00"
##

# Video Options #
VideoFile = ""
VideoLength = 0
TextOverlay = True
#

# Status #
# Camera #
RecordingStatus = False
#
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

def GetVideoFilename():
  global VideoFile
  filenameTime = GetTime().split(":")
  filetime = filenameTime[0] + filenameTime[1]
  VideoFile = "T " + filetime + "  D " + GetDate()
  print ("Filename will be: " + VideoFile)

# Ask For Video Length #
def AskLength():
  global VideoLength
  print ("Enter the length of the video to record (in whole minutes): ")
  lengthquest = raw_input("> ")
  if lengthquest != "":
    try:
      VideoLength = int(lengthquest) * 60	 
    except:
      print ("Value enter is not a valid integer, please try again")
      AskLength()
  else:
    print ("Video length cannot be left blank, please try again")
    AskLength()
#

# Ask For Text Overlay #
def AskOverlay():
  global TextOverlay
  print ("Do you want text overlayed on video?")
  overlayquest = raw_input("y or n > ")
  if overlayquest == "y" or overlayquest == "Y":
    TextOverlay = True
  elif overlayquest == "n" or overlayquest == "N":
    TextOverlay = False
  else:
    print ("Please enter either a 'y' or a 'n'")
    AskOverlay()
#

## I2C ##
def ReadSensor():
  global CurrentTemp
  global CurrentHumidity
  global CurrentMBar
  global CurrentPSI
  try:
    # This section was written by Adafruit Indusdstries and was copied and then modified from the #
    # example file included with the Adafruit BME280 library: #
    # https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280_Example.py #
    temp = sensor.read_temperature()
    humidity = sensor.read_humidity()
    pascals = sensor.read_pressure()
    mbar = pascals / 100 + 12
    psi = mbar * 0.0145037738
    CurrentTemp = format(temp, ".2f")
    CurrentHumidity = format(humidity, ".2f")
    CurrentMBar = format(mbar, ".2f")
    CurrentPSI = format(psi, ".2f")
	# End of Adafruit code #
  except:
      print("Failed to read temperature sensor.")
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
                          "% | Pressure; " + CurrentMBar + "mBar - " + CurrentPSI + "psi"
    return (SensorReadingString)
  except:
    print("Unable to read temperature sensor.") 
    return ("Unable to read temperature sensor.")
#
##

## Camera ##
# Start Recording #
def StartRecord():
  global VideoDirectory
  global VideoFile
  global TextOverlay
  global RecordingStatus
  # Setup WaitToStop thread
  WaitToStopThread = threading.Thread(target=StopRecording)
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
  # Update status file
  UpdateConfigFile('status', 'camera', "True")
  print ("Recording started at: " + GetTime() + "  " + GetDate())
  # Start recording
  Camera.start_recording(VideoDirectory + VideoFile + ".h264", format='h264')
  WaitToStopThread.start()
  if TextOverlay == True:
    WhileRecording()
  else:
    pass
#

# While Recording
def WhileRecording():
  global AnnotationUpdateSpeed
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
      print ("cc-record stopped.")
      UpdateConfigFile('status', 'camera', "False")
      Camera.stop_recording()
      raise
    except:
      print ("Unable to overlay text.")

#

# Stop Recording #
def StopRecording():
  global RecordingStatus
  global VideoLength
  if RecordingStatus:
    Camera.wait_recording(VideoLength)
    Camera.stop_recording()
    RecordingStatus  = False
    UpdateConfigFile('status', 'camera', "False")
    print ("Recording finished at: " + GetTime() + "  " + GetDate())
    sleep(1)
  else:
    pass
#
##
###

### Execute ###
## Get Video Filename From Time/Date ##
GetVideoFilename()
## Ask User For Text Overlay And Length ##
AskLength()
AskOverlay()
##

## Camera ##
StartRecord()
##
###
