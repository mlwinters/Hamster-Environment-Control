### COPYRIGHT ###
# HEC-Setup
# Version: 0.1.0 Alpha
# Copyright (C) 2018 Morgan Winters
# Author: Morgan Winters <morgan.l.winters@gmail.com>
# Contributions:
# Created: 03/09/2018
# Modified By: <name>, <date>
#
# This file is part of Hamster Environment Control.
#
# HEC-Setup is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# HEC-Setup is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HEC-Setup.  If not, see <http://www.gnu.org/licenses/>.
###

### IMPORTS ###
import os
###

### EXECUTE ###
# Create HEC Log File Directory #
os.system("sudo mkdir /home/pi/Hamster-Environment-Control/HEC-Logs")
#

# Create Video File Directory #
os.system("sudo mkdir /home/pi/Hamster-Environment-Control/Videos")
#

# Set hec-status File Permissions #
os.system("sudo chmod 007 /home/pi/Hamster-Environment-Control/hec-status.ini")
#

# Set hec-config File Permissions #
os.system("sudo chmod 007 /home/pi/Hamster-Environment-Control/hec-config.ini")
#

# Update Terminal #
print("Setup done.")
###