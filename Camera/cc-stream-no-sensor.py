### Copyright ###
# Hamster Environment Control
# Version: 0.1.2 Alpha
# Copyright (C) 2018 Morgan Winters <morgan.l.winters@gmail.com
# Author: Morgan Winters
# Contributions: Dave Jones <dave@waveform.org.uk>
# Created: 18/03/2018
# Modified By: <name>, <date>
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
# This software contains code written by Dave Jones. These sections of code 
# where taken from the examples included on the PiCamera website and was released under
# the GNU General Public License Version 2 and can be found here: 
# https://picamera.readthedocs.io/en/release-1.13/
###


### Description ###
# Cage Camera Stream uses the PiCamera Python library to stream a data from the Raspberry Pi Camera Module and pipes it to VLC to 
# be streamed over a local network. PiCamera allows for greater flexibility than just using the raspivid command. It allows
# for the text annotation to be refreshed and changed without stopping the recording. This program displays the time and date,
# white, red and infrared cage light status and updates the text annotation once a second for the duration of the stream.
# This program also uses the VLC library to stream camera data over a local network. VLC media player is then used to view the
# stream from a client desktop/laptop/mobile device by entering "rtsp://<raspi ip address>:8554/" in "Open Network Stream".
# The PiCamera library and VLC need to be installed on your RasPi for this software to run.
###


### IMPORTS ###
import ConfigParser, shlex, subprocess 
import datetime as dt
from time import sleep
import picamera
###

### SETUP ###
## Config Setup ##
StatusFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"  ##### CHANGE THIS IF YOUR hec-status.ini FILE
try:                                                                ##### IS SOMEWHERE ELSE #####
   StatusFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"
   Status = ConfigParser.ConfigParser()
   Status.read(StatusFile)
except:
  print("Unable to load " + StatusFile + ".")
  print("Please make sure it is present and not corrupted and try again.")  ##### CHANGE THIS TO MATCH YOUR
  print ("")                                                                ##### hec-status.ini file LOCATION #####
  print("Cage Camera Record will now exit")
  sleep(2)
  exit()
##


## Variables ##
## Static Variables ##
# Version #
Version = "0.1.2 Alpha"
#

# Pet Name #
PetName = "Tux"  ##### CHANGE THIS TO YOUR PET'S NAME #####
#

# Text Annotation #
AnnotationUpdateSpeed = 1

# Camera #
# This section was written by Dave Jones which was copied and was taken from the #
# examples on the PiCamera website: https://picamera.readthedocs.io/en/release-1.13/ #
Camera = picamera.PiCamera()
# End of Dave Jones code #
VlcCommand = "cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264"
#
##

## Non-Static Variables ##
# Status #
# Camera #
StreamingStatus = False
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

## Camera ##
# Stream Camera
def StreamCamera():
  global StreamingStatus
  global AnnotationUpdateSpeed
  print("Setting up camera...")
  StreamingStatus = True
  UpdateStatusFile('status', 'camera', "True")
  cvlc = subprocess.Popen(shlex.split(VlcCommand), stdin=subprocess.PIPE)
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
  Camera.start_recording(cvlc.stdin, format='h264')
  # End of Dave Jones code #

  while StreamingStatus:
    try:
      # Get HEC system status from HEC status file
      Status.read(StatusFile)
      whitelightstatus = Status.get('status', 'whitelights')
      redlightstatus = Status.get('status', 'redlights')
      irlightstatus = Status.get('status', 'infraredlights')
      climatecontrolstatus = Status.get('status', 'climatecontrol')
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
      print("cc-stream stopped.")
      UpdateStatusFile('status', 'camera', "False")
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