### Copyright ###
# GPIO Controller
# Version: 0.1.0 Alpha
# Copyright (C) 2018 Morgan Winters
# Author: Morgan Winters
# Contributions: 
# Created: 18/03/2018
# Modified By: <name>, <date>
#
# This file is part of Hamster Environment Control.
#
# GPIO Controller is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# GPIO Controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GPIO Controller.  If not, see <http://www.gnu.org/licenses/>.
###


### Description ###
# GPIO Controller is a simple program that allow users to control the cage lighting
# manually outside of HEC.py. As HEC.py runs at startup and due to the cage not having 
# its own monitor and keyboard, this program is run remotely via a SSH connection from 
# another computer/laptop. GPIO Controller will switch the lighting according
# to keyboard commands. It will also update hec-status.ini used by the camera for the
# text annotation on the camera's stream/recording.
###


### Imports ###
import ConfigParser, os
import datetime as dt
from time import sleep
import RPi.GPIO as GPIO
###


### SETUP ###
## Load Status File ##
StatusFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"  ##### CHANGE THIS IF YOUR hec-status.ini FILE
try:                                                                ##### IS SOMEWHERE ELSE #####
  Status = ConfigParser.ConfigParser()
  Status.read(StatusFile)
except:
  print ("Unable to load hec-status.ini.")
  print ("Please ensure it is present in /home/pi/Hamster-Environment-Control/") ##### CHANGE THIS TO MATCH YOUR
  print ("")                                                                     ##### hec-status.ini file LOCATION #####
  print ("GPIO Controller will now exit")
  sleep(2)
  exit()
##

## GPIO Setup ##
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)   # White Lights
GPIO.setup(17, GPIO.OUT)  # Red Lights
GPIO.setup(18, GPIO.OUT)  # Infrared Lights
GPIO.setup(27, GPIO.OUT)  # System Fan
##

## Variables ##
## Static Variables ##
# Version #
Version = "0.1.0 Alpha"
#

# GPIO Pins #
##### CHANGE THESE PIN NUMBER TO SUIT YOU NEEDS #####
WhitePin = 4
RedPin = 17
InfraredPin = 18
SystemFanPin = 27
#
##
###


### FUNCTIONS ###
## System ##
# Get Time #
def GetTime():
  TimeNow = dt.datetime.now()
  time = TimeNow.strftime("%H:%M:%S")
  return (time)
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

## Terminal Screens ##
# Main Screen #
def MainScreen():
  global Version
  os.system("clear")
  print("GPIO Controller")
  print("Version: " + Version)
  print("Copyright (C) 2018 Morgan Winters")
  print("Author: Morgan Winters")
  print("Contributions: ")
  print("Created: 18/03/2018")
  print("")
  print("Type 'help' to view command list.")
  print("")
#

# Copyright #
def ShowCopyright():
  os.system("clear")
  print("   Copyright Notice   ")
  print("______________________")
  print("")
  print("GPIO Controller")
  print("Version: " + Version)
  print("Copyright (C) 2018 Morgan Winters")
  print("Author: Morgan Winters")
  print("Contributions: ")
  print("Created: 18/03/2018")
  print("")
  print("This file is part of Hamster Environment Control.")
  print("")
  print("GPIO Controller is free software: you can redistribute it and/or modify")
  print("it under the terms of the GNU General Public License as published by")
  print("the Free Software Foundation, either version 3 of the License, or")
  print("(at your option) any later version.")
  print("")
  print("GPIO Controller is distributed in the hope that it will be useful,")
  print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
  print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
  print("GNU General Public License for more details.")
  print("")
  print("You should have received a copy of the GNU General Public License")
  print("along with GPIO Controller.  If not, see <https://www.gnu.org/licenses/>.")
  print("")
  print("")
#

# Command List
def ShowCommandList():
  os.system("clear")
  print("   GPIO Controller Command List   ")
  print("__________________________________")
  print("")
  print("Lighting")
  print("(turns gpio pins on/off normally)")
  print("Enable White Lights         white on")
  print("Disable White Lights        white off")
  print("Enable Red Lights           red on")
  print("Disable Red Lights          red off")
  print("Enable IR Lights            ir on")
  print("Disable IR Lights           ir off")
  print("")
  print("Cooling Fans")
  print("Enable System Fan           sys fan on")
  print("Disable System Fan          sys fan off")
  print("")
  print("(turns all other lights off and turns selected colour on)")
  print("Switch To White Lights      white")
  print("Switch To Red Lights        red")
  print("Switch To IR Lights         ir")
  print("")
  print("Misc")
  print("Turn off all GPIO pins      all off")
  print("Show copyright              copyright")
  print("Clear Screen                clear")
  print("Exit                        exit")
  print("")
  print("")
#
##

## GPIO ##
# Toggle White Lights #
def ToggleWhiteLights(_status):
  if _status:
    GPIO.output(WhitePin, True)
  elif not _status:
    GPIO.output(WhitePin, False)
  else:
    GPIO.output(WhitePin, False)
    PrintToFile("ToggleWhiteLights function was called with: " + str(_status) + " which is not a valid boolean value.",\
                "White lights have been turned off.")
    sleep(2)
#

# Toggle Red Lights #
def ToggleRedLights(_status):
  if _status:
    GPIO.output(RedPin, True)
  elif not _status:
    GPIO.output(RedPin, False)
  else:
    GPIO.output(RedPin, False)
    PrintToFile("ToggleRedLights function was called with: " + str(_status) + " which is not a valid boolean value.",\
                "Red lights have been turned off.")
    sleep(2)
#

# Toggle IR Lights #
def ToggleIRLights(_status):
  if _status:
    GPIO.output(InfraredPin, True)
  elif not _status:
    GPIO.output(InfraredPin, False)
  else:
    GPIO.output(InfraredPin, False)
    PrintToFile("ToggleIRLights function was called with: " + str(_status) + " which is not a valid boolean value.",\
                "IR lights have been turned off.")
    sleep(2)
#

# System Fan #
def ToggleSystemFan(_status):
  if _status:
    GPIO.output(SystemFanPin, True)
  elif not _status:
    GPIO.output(SystemFanPin, False)
  else:
    GPIO.output(SystemFanPin, False)
    PrintToFile("ToggleIRLights function was called with: " + str(_status) + " which is not a valid boolean value.",\
                "IR lights have been turned off.")
    sleep(2)
#
##
###


### Execute ###
MainScreen()
###


### UI TERMINAL COMMANDS ###
while 1:
  command = raw_input(">")
  if command == "white on":
    GPIO.output(WhitePin, True)
    UpdateStatusFile('lighting', 'whitelights', "On")
    print("White lights enabled at " + GetTime() + ".")
  elif command == "white off":
    GPIO.output(WhitePin, False)
    UpdateStatusFile('lighting', 'whitelights', "Off")
    print("White lights disabled at " + GetTime() + ".")
  
  elif command == "red on":
    GPIO.output(RedPin, True)
    UpdateStatusFile('lighting', 'redlights', "On")
    print("Red lights enabled at " + GetTime() + ".")
  elif command == "red off":
    GPIO.output(RedPin, False)
    UpdateStatusFile('lighting', 'redlights', "Off")
    print("Red lights disabled at " + GetTime() + ".")

  elif command == "ir on":
    GPIO.output(InfraredPin, True)
    UpdateStatusFile('lighting', 'infraredlights', "On")
    print("IR lights enabled at " + GetTime() + ".")
  elif command == "ir off":
    GPIO.output(InfraredPin, False)
    UpdateStatusFile('lighting', 'infraredlights', "Off")
    print("IR lights disabled at " + GetTime() + ".")

  elif command == "sys fan on":
    GPIO.output(SystemFanPin, True)
    UpdateStatusFile('cooling', 'systemfan', "On")
    print("System Fan enabled at " + GetTime() + ".")
  elif command == "sys fan off":
    GPIO.output(SystemFanPin, False)
    UpdateStatusFile('cooling', 'systemfan', "Off")
    print("System Fan disabled at " + GetTime() + ".")

  elif command == "all off":
    GPIO.output(WhitePin, False)
    GPIO.output(RedPin, False)
    GPIO.output(InfraredPin, False)
    GPIO.output(SystemFanPin, False)
    UpdateStatusFile('lighting', 'whitelights', "Off")
    UpdateStatusFile('lighting', 'redlights', "Off")
    UpdateStatusFile('lighting', 'infraredlights', "Off")
    UpdateStatusFile('cooling', 'systemfan', "Off")
    print("Everything Disabled at " + GetTime() + ".")

  elif command == "white":
    GPIO.output(RedPin, False)
    GPIO.output(InfraredPin, False)
    UpdateStatusFile('lighting', 'redlights', "Off")
    UpdateStatusFile('lighting', 'infraredlights', "Off")
    sleep(1)
    GPIO.output(WhitePin, True)
    UpdateStatusFile('lighting', 'whitelights', "On")
    print("Switched to white lights at " + GetTime() + ".")

  elif command == "red":
    GPIO.output(WhitePin, False)
    GPIO.output(InfraredPin, False)
    UpdateStatusFile('lighting', 'infraredlights', "Off")
    UpdateStatusFile('lighting', 'whitelights', "Off")
    sleep(1)
    GPIO.output(RedPin, True)
    UpdateStatusFile('lighting', 'redlights', "On")
    print("Switched to red lights at " + GetTime() + ".")

  elif command == "ir":
    GPIO.output(WhitePin, False)
    GPIO.output(RedPin, False)
    UpdateStatusFile('lighting', 'whitelights', "Off")
    UpdateStatusFile('lighting', 'redlights', "Off")
    sleep(1)
    GPIO.output(InfraredPin, True)
    UpdateStatusFile('lighting', 'infraredlights', "On") 
    print("Switched to IR lights at " + GetTime() + ".")

  elif command == "copyright":
    ShowCopyright()

  elif command == "help":
    ShowCommandList()

  elif command == "clear":
    MainScreen()

  elif command == "exit":
    print("Closing")
    exit()
