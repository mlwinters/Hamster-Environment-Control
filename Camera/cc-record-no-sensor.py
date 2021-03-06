### COPYRIGHT ###
# Cage Camera Record-no-sensor
# Version: 0.1.5 Alpha
# Copyright (C) 2018 Morgan Winters
# Author: Morgan Winters  <morgan.l.winters@gmail.com>
# Contributions: Dave Jones  <dave@waveform.org.uk>
# Created: 18/03/2018
# Modified By: <name>, <date>
#
# This file is part of Hamster Environment Control.
#
# Cage Camera Record-no-sensor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Cage Camera Record-no-sensor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cage Camera Record-no-sensor.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This software contains code written by Dave Jones. These sections of code 
# where taken from the examples included on the PiCamera website and was released under
# the GNU General Public License Version 2 and can be found here: 
# https://picamera.readthedocs.io/en/release-1.13/
###


### DESCRIPTION ###
# Cage Camera Record-no-sensor uses the PiCamera library to record data from the Raspberry Pi Camera
# Module and saves it to h264 video file. This allows for greater flexiblty than just using the 
# raspivid command. It allows for the text annotation to be refreshed and changed without stopping
# the recording. This program displays the time and date, white, red, infrared cage light status and
# updates the text annotation once a second for the duration of the video.
# PiCamera needs to be installed on your RasPi for this software to run.
###


### IMPORTS ###
import ConfigParser, os, threading
import datetime as dt
from time import sleep
import picamera
###

### SETUP ###
## Config Setup ##
##### CHANGE THIS IF YOUR hec-status.ini FILE IS SOMEWHERE ELSE #####
StatusFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"  
try:
   Status = ConfigParser.ConfigParser()
   Status.read(StatusFile)
except:
  print("Unable to load " + StatusFile + ".")
  ##### CHANGE THIS TO MATCH YOUR hec-status.ini file LOCATION #####
  print("Please make sure it is present and not corrupted and try again.")  
  print ("")
  print("Cage Camera Record will now exit")
  sleep(2)
  exit()
##


## Variables ##
## Static Variables ##
# Version #
Version = "0.1.5 Alpha"
#

# Pet Name #
##### CHANGE THIS TO YOUR PET'S NAME #####
PetName = "Tux"
#

# Text Annotation #
AnnotationUpdateSpeed = 1
#

# Video File #
##### CHANGE THIS IF YOUR YOUR VIDEO FILES SAVED SOMEWHERE ELSE #####
VideoDirectory = "/home/pi/Hamster-Environment-Control/Videos/"  
#

# Camera #
# This section was written by Dave Jones and was taken from the #
# examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
Camera = picamera.PiCamera()
# End of Dave Jones code #
#
##

## Non-Static Variables ##
# Video Options #
VideoFile = ""
VideoLength = 0
TextOverlay = True
#

# Status #
# Camera #
RecordingStatus = False
#
##
###


### FUNCTIONS ###
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

# File IO #
# Update Status File #
def UpdateStatusFile(_section, _parameter, _value):
  try:
    Status.set(_section, _parameter, _value)
    with open(StatusFile, 'wb') as tempstatus:
      Status.write(tempstatus)
  except:
    print("Unable to write to hec-status.ini")
    print("Please check it is located in: " + StatusFile)
#
##

## User Options ##
# Get Video Filename #
def GetVideoFilename():
  global VideoFile
  filenameTime = GetTime().split(":")
  filetime = filenameTime[0] + filenameTime[1]
  VideoFile = "T" + filetime + "-D" + GetDate()
  print ("Filename will be: " + VideoFile)
#

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
  UpdateStatusFile('camera', 'camerastatus', "Recording")
  print ("Recording started at: " + GetTime() + "  " + GetDate())
  # Set camera capture options
  # This section was written by Dave Jones which was copied and then modified from the #
  # examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
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
  Camera.start_recording(VideoDirectory + VideoFile + ".h264", format='h264')
  # End of Dave Jones code #
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
      Status.read(StatusFile)
      whitelightstatus = Status.get('lighting', 'whitelights')
      redlightstatus = Status.get('lighting', 'redlights')
      irlightstatus = Status.get('lighting', 'infraredlights')
      climatecontrolstatus = Status.get('climate', 'climatecontrol')
      # Overlay text to stream
      # This section was written by Dave Jones which was copied and then modified from the #
      # examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
      Camera.annotate_text = PetName + " Cage-Cam\n\nTime; " + GetTime() + " (BST) | Date; " + \
                             GetDay() + " " + GetDate() + "\nWhite Lights; " + whitelightstatus + \
                             " | Red Lights; " + redlightstatus + " | Infrared Lights; " + irlightstatus + \
                             " | Climate Control; " + climatecontrolstatus
      # End of Dave Jones code #
      sleep(AnnotationUpdateSpeed)
    except KeyboardInterrupt:
      print ("cc-record stopped.")
      UpdateStatusFile('camera', 'camerastatus', "False")
      # This section was written by Dave Jones which was copied and then modified from the #
      # examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
      Camera.stop_recording()
      # End of Dave Jones code #
      raise
    except:
      print ("Unable to overlay text.")

#

# Stop Recording #
def StopRecording():
  global RecordingStatus
  global VideoLength
  if RecordingStatus:
    # This section was written by Dave Jones which was copied and then modified from the #
    # examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
    Camera.wait_recording(VideoLength)
    Camera.stop_recording()
    # End of Dave Jones code #
    RecordingStatus  = False
    UpdateStatusFile('camera', 'camerastatus', "False")
    print ("Recording finished at: " + GetTime() + "  " + GetDate())
    sleep(1)
  else:
    pass
#
##
###

### EXECUTE ###
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
