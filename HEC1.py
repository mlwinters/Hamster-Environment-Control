### COPYRIGHT ###
# Hamster Environment Control
# Version: 0.1.0 Alpha
# Copyright (C) 2018 Morgan Winters
# Author: Morgan Winters <morgan.l.winters@gmail.com>
# Contributions: Adafruit Industries
# Created: 18/03/2018
# Modified By: <name>, <date>
#
# This file is part of Hamster Environment Control.
#
# Hamster Environment Control is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Hamster Environment Control is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hamster Environment Control.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This software contains code written by Adafruit Industires. These sections of code
# where taken from the example included with the BME280 library which was released under
# the MIT license and can be found here:
# https://github.com/adafruit/Adafruit_Python_BME280
###


### DESCRIPTION ###
# HEC.py is the core software that controls a computerised hamster cage.
# It controls the automatic lighting and switches either the white or red cages lights
# depending on the time of day as well as switches the infrared cage lights on during the
# night time but only if the camera is running. HEC also monitors the temperature
# of the cage and reports in the log file and updates the hec-status.ini file used by
# the camera when the temperature is outside of an ideal range. The temperature is also
# logged every 30 minutes. HEC.py will also create a new log file at startup
# (if file of current date doesn't exist) and a new subfolder of
# "home/pi/Hamster-Environment-Control/HEC-Logs/" every week. HEC.py will restart the 
# Raspberry Pi every day at midnight to ensure system stability.
###


### IMPORTS ###
import ConfigParser, os, threading, time
import datetime as dt
from os import path
from time import sleep
from Adafruit_BME280 import *
import RPi.GPIO as GPIO
###

# Clear and update terminal
os.system("clear")
print ("Starting Hamster Environment Control,")
print ("Please wait...")
sleep(0.25)
#

### SETUP ###
## Setup Status File ##
##### CHANGE THIS IF YOUR hec-status.ini FILE IS SOMEWHERE ELSE #####
StatusFile = "/home/pi/Hamster-Environment-Control/hec-status.ini"
try:
  Status = ConfigParser.ConfigParser()
  Status.read(StatusFile)
except:
  print ("Unable to load hec-status.ini.")
  ##### CHANGE THIS TO MATCH YOUR hec-status.ini file LOCATION #####
  print ("Please ensure it is present in /home/pi/Hamster-Environment-Control/")
  print ("")
  print ("Hamster Environment Control will now exit")
  sleep(2)
  exit()
##

## Setup Config File ##
##### CHANGE THIS IF YOUR hec-config.ini FILE IS SOMEWHERE ELSE #####
ConfigFile = "/home/pi/Hamster-Environment-Control/hec-config.ini"
try:
  Config = ConfigParser.ConfigParser()
  Config.read(ConfigFile)
except:
  print ("Unable to load hec-config.ini.")
  ##### CHANGE THIS TO MATCH YOUR hec-config.ini file LOCATION #####
  print ("Please ensure it is present in /home/pi/Hamster-Environment-Control/")
  print ("")                                                                     
  print ("Hamster Environment Control will now exit")
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

# Ensure GPIO pins are low
GPIO.output(4, False)
GPIO.output(17, False)
GPIO.output(18, False)
GPIO.output(27, False)
#
##

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
Version = "0.1.0 Alpha"
#

# GPIO Pins #
##### CHANGE THESE PIN NUMBERS TO SUIT YOU NEEDS #####
WhitePin = 4
RedPin = 17
InfraredPin = 18
SystemFanPin = 27
#

# Temperature Settings #
MinTemp = str(Config.get('climate', 'mintemp'))
NormalTemp = str(Config.get('climate', 'normaltempmin')), str(Config.get('climate', 'normaltempmax'))
MaxTemp = str(Config.get('climate', 'maxtemp'))
#

# Cage Light Times #
WhiteTimes = str(Config.get('lighting', 'whiteontime')), str(Config.get('lighting', 'whiteofftime'))
RedTimes = str(Config.get('lighting', 'redontime')), str(Config.get('lighting', 'redofftime'))
IRTimes = str(Config.get('lighting', 'irontime')), str(Config.get('lighting', 'irofftime'))
#

# Thread Update Times #
ClimateControlUpdateTime = int(Config.get('threads', 'climateupdatetime'))
CageLightsUpdateTime = int(Config.get('threads', 'cagelightupdatetime'))
HousekeepingUpdateTime = int(Config.get('threads', 'housekeepingupdatetime'))
#

# System Logs #
##### CHANGE THIS IF YOU WANT THE LOG FILES TO BE SAVED SOMEWHERE ELSE. #####
SystemLogFileDirectory = "/home/pi/Hamster-Environment-Control/HEC-Logs/" 
#

# System Reboot Time #
SystemRebootTime = str(Config.get('housekeeping', 'systemreboottime'))
#
##

## Non-Static Variables ##
# GPIO Status's #
WhiteLightStatus = False
RedLightStatus = False
IRLightStatus = False
SystemFanStatus = False
#

# Sensor Readings #
CurrentTemp = "00.00"      # Temperature in degrees celsius
CurrentHumidity = "00.00"  # Relative humidity in percent 
CurrentMBar = "0000.00"    # Air pressure in millibar
CurrentPSI = "00.00"       # Air pressure in pound per square inch
#

# Threads #
##### SET THESE TO FALSE TO DISABLE THREAD #####
HousekeepingThread = True
ClimateControlThread = True
AutoCageLightThread = True
#

# System Logs #
SystemLogFile = "HEC Log - "
##### CHANGE THIS IF YOU DON'T WANT SYSTEM EVENTS TO BE LOGGED #####
LogSystemEvents = True
ClimateDataLogged = False
CameraStatusLogged = False
#

## Status's ##
# System #
ClimateControlStatus = "False"
AutoCageLightStatus = "False"
CameraStatus = "False"
#
##
###


### FUNCTIONS ###
## System ##
# Get Date / Time / Day #
def GetTime():
  TimeNow = dt.datetime.now()
  time = TimeNow.strftime("%H:%M:%S")
  return (time)

def GetMinSec():
  MinSecNow = dt.datetime.now()
  minsec = MinSecNow.strftime("%M:%S")
  return (minsec)

def GetDate():
  DateNow = dt.datetime.now()
  date = DateNow.strftime("%d-%m-%Y")
  return (date)

def GetDay():
  DayNow = dt.datetime.now()
  day = DayNow.strftime("%a")
  return (day)
#

# Cleanup #
def CleanUp():
  global ClimateControlThread
  global HousekeepingThread
  global AutoCageLightThread
  ClimateControlThread = False
  HousekeepingThread = False
  AutoCageLightThread = False
  sleep(5)
  ToggleWhiteLights(False)
  ToggleRedLights(False)
  ToggleIRLights(False)
  ToggleSystemFan(False)
  UpdateStatusFile('lighting', 'whitelights', "Off")
  UpdateStatusFile('lighting', 'redlights', "Off")
  UpdateStatusFile('lighting', 'infraredlights', "Off")
  UpdateStatusFile('climate', 'climatecontrol', "HEC Not Running")
  UpdateStatusFile('camera', 'camerastatus', "False")
#

# Exit HEC #
def HECExit():
  print("Closing, please wait...")
  CleanUp()
  GPIO.cleanup()
  print("Cleanup done...")
  print("Closing")
#
##

## File IO ##
# Update Status File #
def UpdateStatusFile(_section, _parameter, _value):
  try:
    Status.set(_section, _parameter, _value)
    with open(StatusFile, 'wb') as tempstatus:
      Status.write(tempstatus)
  except:
    print("Unable to write to hec-status.ini")
    print("Please check: " + StatusFile)
    PrintToFile("Unable to write to hec-status.ini", "Please check it is located in: " + StatusFile)
#

# Update Config File #
def UpdateConfigFile(_section, _parameter, _value):
  try:
    Config.set(_section, _parameter, _value)
    with open(ConfigFile, 'wb') as tempconfig:
      Config.write(tempconfig)
  except:
    print("Unable to write to hec-config.ini")
    print("Please check: " + ConfigFile)
    PrintToFile("Unable to write to hec-config.ini", "Please check it is located in: " + ConfigFile)
#

# Refresh Variables From Config File #
def RefreshVariables():
  global MinTemp
  global NormalTemp
  global MaxTemp
  global WhiteTimes
  global RedTimes
  global IRTimes
  global ClimateControlUpdateTime
  global CageLightsUpdateTime
  global HousekeepingUpdateTime
  global SystemRebootTime

  Config.read(ConfigFile)
  MinTemp = str(Config.get('climate', 'mintemp'))
  NormalTemp = str(Config.get('climate', 'normaltempmin')), str(Config.get('climate', 'normaltempmax'))
  MaxTemp = str(Config.get('climate', 'maxtemp'))
  WhiteTimes = str(Config.get('lighting', 'whiteontime')), str(Config.get('lighting', 'whiteofftime'))
  RedTimes = str(Config.get('lighting', 'redontime')), str(Config.get('lighting', 'redofftime'))
  IRTimes = str(Config.get('lighting', 'irontime')), str(Config.get('lighting', 'irofftime'))
  ClimateControlUpdateTime = int(Config.get('threads', 'climateupdatetime'))
  CageLightsUpdateTime = int(Config.get('threads', 'cagelightupdatetime'))
  HousekeepingUpdateTime = int(Config.get('threads', 'housekeepingupdatetime'))
  SystemRebootTime = str(Config.get('housekeeping', 'systemreboottime'))
#

# First Start #
def CheckFirstStart():
  global SystemLogFileDirectory
  global SystemLogFile
  try:
    # Check if this is first start, if so set up log directory
    Status.read(StatusFile)
    FirstStart = Status.get('firststart', 'firststart')
    if FirstStart == "True":
      directory = SystemLogFileDirectory + GetDate() + "/"
      os.system("sudo mkdir " + directory)
      SystemLogFileDirectory = directory
      SystemLogFile = "HEC-Log-" + GetDate() + ".txt"
      UpdateConfigFile('logfile', 'logdirctory', SystemLogFileDirectory)
      UpdateConfigFile('logfile', 'logfile', SystemLogFile)
      UpdateStatusFile('firststart', 'firststart', "False")
  except:
    print("Unable to setup up log file. Please check hec-status,")
    print("hec-config and " + SystemLogFileDirectory)
#

# Setup Log File #
def SetupLogFile():
  global SystemLogFileDirectory
  global SystemLogFile
  try:
    # Set up log file and its directory
    directory = SystemLogFileDirectory + GetDate() + "/"
    if GetDay() == "Mon" and GetTime() >= "00:00" and GetTime() <= "00:05":
      if not os.path.exists(directory):
        os.system("sudo mkdir " + directory)
        SystemLogFileDirectory = directory
        SystemLogFile = "HEC-Log-" + GetDate() + ".txt"
        UpdateConfigFile('logfile', 'logdirctory', SystemLogFileDirectory)
        UpdateConfigFile('logfile', 'logfile', SystemLogFile)
    else:
      Config.read(ConfigFile)
      SystemLogFileDirectory = Config.get('logfile', 'logdirctory')
      SystemLogFile = "HEC-Log-" + GetDate() + ".txt"
      UpdateConfigFile('logfile', 'logfile', SystemLogFile)
    print("Log file is: " + SystemLogFileDirectory + SystemLogFile)
  except:
    print("Unable to setup up log file. Please check hec-status,")
    print("hec-config and " + SystemLogFileDirectory)
#

# Print Event To Log File #
def PrintToFile(_message, _details):
  global SystemLogFileDirectory
  global SystemLogFile
  global LogSystemEvents
  if LogSystemEvents:
    try:
      dateString = "Date: " + GetDate()
      timeString = "Time: " + GetTime()
      messageString = "Message: "
      detailsString = "Details: "
      with open(SystemLogFileDirectory + SystemLogFile, "a+") as logFile:
        logFile.writelines("%s\n%s\n%s\n%s\n\n\n" % (dateString, timeString, \
                           messageString + _message, detailsString + _details))
        logFile.close()
    except:
      print("Failed to make entry into log file. Please check:")
      print(SystemLogFileDirectory + SystemLogFile)
  else:
    pass
#
##

## Terminal Screens ##
# Main Screen #
def MainScreen():
  global Version
  os.system("clear")
  print("Hamster Environment Control")
  print("Version: " + Version)
  print("Copyright (C) 2018 Morgan Winters")
  print("Author: Morgan Winters")
  print("Contributions: Adafruit Industries")
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
  print("Hamster Environment Control")
  print("Version: " + Version)
  print("Copyright (C) 2018 Morgan Winters")
  print("Author: Morgan Winters")
  print("Contributions: Adafruit Industries")
  print("Created: 18/03/2018")
  print("")
  print("Hamster Environment Control is free software: you can redistribute it and/or modify")
  print("it under the terms of the GNU General Public License as published by")
  print("the Free Software Foundation, either version 3 of the License, or")
  print("(at your option) any later version.")
  print("")
  print("Hamster Environment Control is distributed in the hope that it will be useful,")
  print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
  print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
  print("GNU General Public License for more details.")
  print("")
  print("You should have received a copy of the GNU General Public License")
  print("along with Hamster Environment Control.  If not, see <https://www.gnu.org/licenses/>.")
  print("")
  print("")
  print("This software contains code written by Adafruit Industires.")
  print("These sections of code where taken from the example included")
  print("with the BME280 library which was released under the MIT license")
  print("and can be found here: https://github.com/adafruit/Adafruit_Python_BME280")
  print("")
  print("")
#

# Command List
def ShowCommandList():
  os.system("clear")
  print("   HEC Command List   ")
  print("______________________")
  print("")
  print("System")
  print("Show System Time                  time")
  print("Show System Date                  date")
  print("Show Sensor Readings              sensor")
  print("Clear Screen                      clear")
  print("Show Command List                 help")
  print("Show Copyright Notice             copyright")
  print("Exit HEC                          exit")
  print("Reboot Raspberry Pi               reboot")
  print("Shutdown Raspberry Pi             shutdown")
  print("")
  print("Lighting")
  print("Enable White Lights               white on")
  print("Disable White Lights              white off")
  print("Enable Red Lights                 red on")
  print("Disable Red Lights                red off")
  print("Enable IR Lights                  ir on")
  print("Disable IR Lights                 ir off")
  print("")
  print("Cooling")
  print("Enable System Fan                 sys fan on")
  print("Disable System Fan                sys fan off")
  print("")
  print("Threads")
  print("Start Housekeeping                start housekeeping")
  print("Stop Housekeeping                 stop housekeeping")
  print("Start Climate Control             start climate control")
  print("Stop Climate Control              stop climate control")
  print("Start Auto Lighting               start auto lights")
  print("Stop Auto Lighting                stop auto lights")
  print("")
  print("Status")
  print("Get Housekeeping Thread Status    housekeeping thread status")
  print("Get Climate Thread Status         climate thread status")
  print("Get Climate Control Status        climate status")
  print("Get Lighting Thread Status        lighting thread status")
  print("Get Lighting Status               lighting status")
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
    PrintToFile("ToggleWhiteLights function was called with: " + str(_status) + \
                " which is not a valid boolean value.", "White lights have been turned off.")
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
    PrintToFile("ToggleRedLights function was called with: " + str(_status) + \
                " which is not a valid boolean value.", "Red lights have been turned off.")
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
    PrintToFile("ToggleIRLights function was called with: " + str(_status) + \
                " which is not a valid boolean value.", "IR lights have been turned off.")
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
    PrintToFile("ToggleIRLights function was called with: " + str(_status) + \
                " which is not a valid boolean value.", "System fan has been turned off.")
    sleep(2)
#

## I2C ##
# Temperature Sensor #
def ReadSensor():
  global CurrentTemp
  global CurrentHumidity
  global CurrentMBar
  global CurrentPSI
  try:
    # This section was written by Adafruit Indusdstries which was copied and then modified from the #
    # example file included with the Adafruit BME280 library: #
    # https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280_Example.py #
    temp = sensor.read_temperature()
    humidity = sensor.read_humidity()
    pascals = sensor.read_pressure()
    ##### plus 12 for altitude compensation, change the "+ 12" to suit your local altitude #####
    mbar = pascals / 100 + 12
    psi = mbar * 0.0145037738
    CurrentTemp = format(temp, ".2f")
    CurrentHumidity = format(humidity, ".2f")
    CurrentMBar = format(mbar, ".2f")
    CurrentPSI = format(psi, ".2f")
	# End of Adafruit code #
  except:
    print("Failed to read temperature sensor.")
    PrintToFile("Failed to read temperature sensor.", "")
    sleep(2)
#

# Return Sensor Reading As A String #
def GetSensorReading():
  global CurrentTemp
  global CurrentHumidity
  global CurrentMBar
  global CurrentPSI
  ReadSensor()
  sensorReadingString = "Temperature: " + CurrentTemp + "C | Relative Humidity: " + \
                        CurrentHumidity + "% | Pressure: " + CurrentMBar + "mBar - " + \
                        CurrentPSI + "psi"
  return (sensorReadingString)
#
##

## Background Thread Functions ##
# Housekeeping #
def Housekeeping():
  global SystemRebootTime
  global CameraStatus
  global CameraStatusLogged
  global HousekeepingUpdateTime
  global HousekeepingThread

  while HousekeepingThread:
    # Check time for system reboot
    if GetTime() == SystemRebootTime:
      print("HEC going for it's daily reboot. New log file will be created after restart.")
      PrintToFile("System housekeeping, HEC going for it's daily reboot", "New log file will be created after restart.")
      CleanUp()
      HECExit()
      os.system("sudo reboot")
      exit()

    # Save temperature sensor data to log file every 30 minutes
    if GetMinSec() == "00:00" or GetMinSec() == "30:00":
      print("Cage temperature update:", GetSensorReading())
      PrintToFile("Cage temperature update:", GetSensorReading())

    # Refresh Variables
    RefreshVariables()

    # Get Camera Status
    Status.read(StatusFile)
    CameraStatus = Status.get('camera', 'camerastatus')

    sleep(HousekeepingUpdateTime)
  else:
    print("Housekeeping thread has been stopped")
    PrintToFile("Housekeeping thread has been stopped.", "")
#

# Climate Control #
def ClimateControl():
  global MinTemp
  global NormalTemp
  global MaxTemp
  global CurrentTemp
  global ClimateControlThread
  global ClimateControlStatus
  global ClimateControlUpdateTime
  global ClimateDataLogged

  while ClimateControlThread:
    ReadSensor()
    while CurrentTemp <= MinTemp and ClimateControlThread:
      if not ClimateDataLogged:
        ToggleSystemFan(False)
        ClimateControlStatus = "Too Low"
        print("Cage temperature is too low!\n" + GetSensorReading())
        PrintToFile("Cage temperature is too low!", GetSensorReading())
        UpdateStatusFile('climate', 'climatecontrol', "TOO LOW!")
        ClimateDataLogged = True
      else:
        pass
      sleep(ClimateControlUpdateTime)
      ReadSensor()
    else:
      ClimateDataLogged = False

    while CurrentTemp >= NormalTemp[0] and CurrentTemp <= NormalTemp[1] and ClimateControlThread:
      if not ClimateDataLogged:
        ToggleSystemFan(False)
        ClimateControlStatus = "Running"
        print("Cage is at an ideal temperature.\n" + GetSensorReading())
        PrintToFile("Cage is at an ideal temperature.", GetSensorReading())
        UpdateStatusFile('climate', 'climatecontrol', "Running")
        ClimateDataLogged = True
      else:
        pass
      sleep(ClimateControlUpdateTime)
      ReadSensor()
    else:
      ClimateDataLogged = False

    while CurrentTemp >= MaxTemp and ClimateControlThread:
      if not ClimateDataLogged:
        ToggleSystemFan(True)
        ClimateControlStatus = "Too High"
        print("Cage temperature is too high!\n" + GetSensorReading())
        PrintToFile("Cage temperature is too high!", GetSensorReading())
        UpdateStatusFile('climate', 'climatecontrol', "TOO HIGH!")
        ClimateDataLogged = True
        sleep(ClimateControlUpdateTime)
      else:
       pass
      sleep(ClimateControlUpdateTime)
      ReadSensor()
    else:
      ClimateDataLogged = False

    sleep(ClimateControlUpdateTime)
  else:
    ClimateControlStatus = "False"
    print("Climate control thread has been stopped")
    PrintToFile("Climate control thread has been stopped.", "")
#

# Automatic Visible Cage Lights #
def AutoCageLight():
  global WhiteTimes
  global RedTimes
  global IRTimes
  global WhiteLightStatus
  global RedLightStatus
  global IRLightStatus
  global CameraStatus
  global AutoCageLightStatus
  global ClimateControlStatus
  global CageLightsUpdateTime
  global AutoCageLightThread

  while AutoCageLightThread:
    AutoCageLightStatus = True
    # Automatic White lights
    if GetTime() >= WhiteTimes[0] and GetTime() <= WhiteTimes[1]:
      if not WhiteLightStatus:
        WhiteLightStatus = True
        ToggleWhiteLights(True)
        ToggleSystemFan(True)
        AutoCageLightStatus = "White"
        print("White lights activated")
        PrintToFile("White lights activated.", GetSensorReading())
        UpdateStatusFile('lighting', 'whitelights', "On")
      else:
	    pass
    else:
      if WhiteLightStatus:
        WhiteLightStatus = False
        ToggleWhiteLights(False)
        ToggleSystemFan(False)
        AutoCageLightStatus = "Running"
        print("White lights deactivated")
        PrintToFile("White lights deactivated.", GetSensorReading())
        UpdateStatusFile('lighting', 'whitelights', "Off")
      else:
	    pass

    # Automatic red lights
    if GetTime() >= RedTimes[0] and GetTime() <= RedTimes[1]:
      if not RedLightStatus:
        RedLightStatus = True
        ToggleRedLights(True)
        AutoCageLightStatus = "Red"
        print("Red lights activated")
        PrintToFile("Red lights activated.", GetSensorReading())
        UpdateStatusFile('lighting', 'redlights', "On")
      else:
	    pass
    else:
      if RedLightStatus:
        RedLightStatus = False
        ToggleRedLights(False)
        AutoCageLightStatus = "Running"
        print("Red lights deactivated")
        PrintToFile("Red lights deactivated.", GetSensorReading())
        UpdateStatusFile('lighting', 'redlights', "Off")
      else:
	    pass

    # Automatic infrared lights
    # IR lights are only enabled if the camera is either recording or streaming
    if GetTime() >= IRTimes[0] and GetTime() <= IRTimes[1]:
      if CameraStatus == "Streaming" or CameraStatus == "Recording":
        if not IRLightStatus:
          IRLightStatus = True
          ToggleIRLights(True)
          ToggleSystemFan(True)
          AutoCageLightStatus = "IR"
          print("Camera started, IR lights activated")
          PrintToFile("Camera started, infrared lights activated.", GetSensorReading())
          UpdateStatusFile('lighting', 'infraredlights', "On")
        else:
          pass
      else:
        if IRLightStatus:
          IRLightStatus = False
          ToggleIRLights(False)
          ToggleSystemFan(False)
          AutoCageLightStatus = "Running"
          print("Camera stopped, IR lights deactivated")
          PrintToFile("Camera stopped, infrared lights deactivated.", GetSensorReading())
          UpdateStatusFile('lighting', 'infraredlights', "Off")
        else:
	      pass
    else:
      if IRLightStatus:
        IRLightStatus = False
        ToggleIRLights(False)
        ToggleSystemFan(False)
        AutoCageLightStatus = "Running"
        print("Camera still running but infrared lights deactivated as scheduled.")
        PrintToFile("Camera still running but infrared lights deactivated as scheduled.", GetSensorReading())
        UpdateStatusFile('lighting', 'infraredlights', "Off")
      else:
	    pass
    sleep(CageLightsUpdateTime)

  else:
    AutoCageLightStatus = False
    ToggleWhiteLights(False)
    ToggleRedLights(False)
    ToggleIRLights(False)
    AutoCageLightStatus = "False"
    UpdateStatusFile('lighting', 'whitelights', "Off")
    UpdateStatusFile('lighting', 'redlights', "Off")
    UpdateStatusFile('lighting', 'infraredlights', "Off")
    if ClimateControlStatus == "Running" or ClimateControlStatus == "Too Low":
      ToggleSystemFan(False)
      UpdateStatusFile('cooling', 'systemfan', "Off")
    print("Cage lighting thread has been stopped.")
    PrintToFile("Cage lighting thread has been stopped.", "")
#
##
###


### EXECUTE###
## Setup Log File ##
print ("Setting up log file...")
# Check if this is first start
CheckFirstStart()
#

# Setup log file
SetupLogFile()
#

# Update log file
PrintToFile("Hamster Environment Control   -   Version: " + Version, "Start of system log.")
#
##

## Start threads ##
# Setup and start Housekeeping, ClimateControl and AutoCageLight functions
# as seperate background threads.
# Housekeeping #
if HousekeepingThread:
  print("Starting housekeeping thread...")
  try:
    HousekeepThread = threading.Thread(target=Housekeeping)
    HousekeepThread.start()
  except:
    print("Error starting housekeeping thread.")
    PrintToFile("Error starting housekeeping thread.", "Thread not running.")
    sleep(2.5)
#

# Climate Control #
if ClimateControlThread:
  print("Starting climate control thread...")
  try:
    ClimateThread = threading.Thread(target=ClimateControl)
    ClimateThread.start()
  except:
    print("Error starting climate control thread.")
    PrintToFile("Error starting climate control thread.", "Thread not running.")
    sleep(2.5)
#

# Auto Cage Lights #
if AutoCageLightThread:
  print("Starting automatic cage lights thread...")
  try:
    LightingThread = threading.Thread(target=AutoCageLight)
    LightingThread.start()
  except:
    print("Error starting automatic cage lights thread.")
    PrintToFile("Error starting automatic cage lights thread.", "Thread not running.")
    sleep(2.5)
#
##

## Update Terminal ##
print("")
print ("Loading complete.")
sleep(1)
##

## Show Main Screen ##
MainScreen()
##
###


### MAIN UI THREAD ###
while True:
  command = raw_input("> ")
  # Time
  if command == "time":
    print("The time is: " + GetTime())

  # Date
  elif command == "date":
    print("The date is: " + GetDate())

  # Sensor
  elif command == "sensor":
    print(GetSensorReading())

  # Clear Screen
  elif command == "clear":
    MainScreen()

  # Show Command List
  elif command == "help":
    ShowCommandList()

  # Show Copyright Notice
  elif command == "copyright":
    ShowCopyright()

  # Exit HEC
  elif command == "exit":
    HECExit()
    exit()

  # Restart RasPi
  elif command == "reboot":
    print("Restarting, please wait...")
    HECExit()
    os.system("sudo reboot")
    exit()

  # Shutdown RasPi
  elif command == "shutdown":
    print("Shutting down, please wait...")
    HECExit()
    os.system("sudo shutdown -h now")
    exit()

  # Enable White Lights
  elif command == "white on":
    print("White lights enabled at: " + GetTime())
    ToggleWhiteLights(True)
    UpdateStatusFile('lighting', 'whitelights', "On")

  # Disable White Lights
  elif command == "white off":
    print("White lights disabled at: " + GetTime())
    ToggleWhiteLights(False)
    UpdateStatusFile('lighting', 'whitelights', "Off")

  # Enable Red Lights
  elif command == "red on":
    print("Red lights enabled at: " + GetTime())
    ToggleRedLights(True)
    UpdateStatusFile('lighting', 'redlights', "On")

  # Disable Red Lights
  elif command == "red off":
    print("Red lights disabled at: " + GetTime())
    ToggleRedLights(False)
    UpdateStatusFile('lighting', 'redlights', "Off")

  # Enable IR Lights
  elif command == "ir on":
    print("IR lights enabled at: " + GetTime())
    ToggleIRLights(True)
    UpdateStatusFile('lighting', 'infraredlights', "On")

  # Disable IR Lights
  elif command == "ir off":
    print("IR lights disabled at: " + GetTime())
    ToggleIRLights(False)
    UpdateStatusFile('lighting', 'infraredlights', "Off")

  # Enable System Fan
  elif command == "sys fan on":
    print("System fan enabled at: " + GetTime())
    ToggleSystemFan(True)
    UpdateStatusFile('cooling', 'systemfan', "On")

  # Disable System Fan
  elif command == "sys fan off":
    print("System fan enabled at: " + GetTime())
    ToggleSystemFan(False)
    UpdateStatusFile('cooling', 'systemfan', "Off")

  # Start House Keeping Thread
  elif command == "start housekeeping":
    if not HousekeepingThread:
      print("Starting housekeeping thread...")
      try:
        HousekeepThread = threading.Thread(target=Housekeeping)
        HousekeepThread.start()
      except:
        print("Error starting housekeeping thread.")
        sleep(2.5)
    else:
      print("Housekeeping thread is already running.")

  # Stop House Keeping Thread
  elif command == "stop housekeeping":
    HousekeepingThread = False
    sleep(1)

  # Start Climate Control Thread
  elif command == "start climate control":
    if not ClimateControlThread:
      print("Starting climate control thread...")
      try:
        ClimateThread = threading.Thread(target=ClimateControl)
        ClimateThread.start()
      except:
        print("Error starting climate control thread.")
        sleep(2.5)
    else:
      print("Climate control thread is already running.")

  # Stop Climate Control Thread
  elif command == "stop climate control":
    ClimateControlThread = False
    sleep(1)

  # Start Auto Cage Light Thread
  elif command == "start auto lights":
    if not AutoCageLightThread:
      print("Starting automatic cage lights thread...")
      try:
        LightingThread = threading.Thread(target=AutoCageLight)
        LightingThread.start()
      except:
        print("Error starting automatic cage lights thread.")
        sleep(2.5)
    else:
      print("Auto cage light thread is already running.")

  # Stop Auto Cage Light Thread
  elif command == "stop auto lights":
    AutoCageLightThread = False
    sleep(1)

  # Get Housekeeping Thread Status
  elif command == "housekeeping thread status":
    print("Housekeeping thread status: " + HousekeepingThread)

  # Get Climate Control Thread Status
  elif command == "climate thread status":
    print("Climate thread status: " + ClimateControlThread)

  # Get Climate Contol Status
  elif command == "climate status":
    print("Lighting status: " + ClimateControlStatus)

  # Get Lighting Thread Status
  elif command == "lighting thread status":
    print("Lighting thread status: " + AutoCageLightThread)

  # Get Lighting Status
  elif command == "lighting status":
    print("Lighting status: " + AutoCageLightStatus)

  else:
    print("Unknown command, type help to see command list and try again.")

###