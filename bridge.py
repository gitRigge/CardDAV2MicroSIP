# The MIT License (MIT)
# 
# Copyright (c) 2015, Roland Rickborn (r_2@gmx.net)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Revision history:
# 2015-09-30  Created
#
# Requirements:
# This script requires the CardDAV CLI client pyCardDAV to be installed!
# Get it from here: https://github.com/geier/pycarddav
#
# This script generates Contacts.xml valid for MicroSIP VoIP client v3.10
# ---------------------------------------------------------------------------

import subprocess
import shutil
import string
import os
import time
__author__ = 'Roland Rickborn'

#######################################
### DO SOME CHANGES BELOW THIS LINE ###
#######################################
# Settings
myLocalCountryCode = "+49"
catHome = "Home"
catMobile = "Mobil"
catWork = "Arbeit"
cfgFile = "pycard.conf"
#######################################
### DO SOME CHANGES ABOVE THIS LINE ###
#######################################

# Path to MicroSIP XML file
microSipDataPath = os.environ['APPDATA']+"\MicroSIP"

# Sync data
subprocess.call(['c:\Python27\python.exe','c:\Python27\Scripts\pycardsyncer',
                                  '-c',cfgFile])

# Read data
retval = subprocess.check_output(['c:\Python27\python.exe','c:\Python27\Scripts\pc_query',
                                  '-c',cfgFile,'-A'])

# Split initial welcome text
tmp = string.split(retval,"searching for ...\r\n")
tmp = string.replace(tmp[1],"\r","")

# Get raw contact data
contact_raw = string.split(tmp,"Name: ")

# Destill required contact data
countryCodeReplacement = myLocalCountryCode + " "
contacts = []
for item1 in contact_raw:
    try:
        has_phone_work = 0
        has_phone_mobil = 0
        has_phone_home = 0
        telhome = 0
        telmobil = 0
        telwork = 0
        tmp_item = string.split(item1,"\n")
        name_raw = tmp_item[0]
        if name_raw.find(",") >= 0:
            tmp = string.split(name_raw,",")
            vorname = tmp[1].strip()
            nachname = tmp[0].strip()
        else:
            tmp = string.split(name_raw," ")
            vorname = tmp[0].strip()
            name_raw = string.join(tmp[1:]," ")
            nachname = name_raw.strip()
        for item2 in tmp_item:
            if item2.startswith("TEL"):
                if item2.find("WORK") >= 0 and item2.find("VOICE") >= 0:
                    tmp = string.split(item2,":")
                    telwork_raw = string.replace(tmp[1]," ","")
                    telwork_raw = string.replace(telwork_raw,"-","")
                    telwork_raw = string.replace(telwork_raw,"(","")
                    telwork_raw = string.replace(telwork_raw,")","")
                    telwork_raw = "%s %s" % (telwork_raw[0:3],telwork_raw[3:])
                    telwork = string.replace(telwork_raw,countryCodeReplacement,"0")
                    if len(telwork) > 3:
                        has_phone_work = 1
                elif item2.find("CELL") >= 0 and item2.find("VOICE") >= 0:
                    tmp = string.split(item2,":")
                    telmobil_raw = string.replace(tmp[1]," ","")
                    telmobil_raw = string.replace(telmobil_raw,"-","")
                    telmobil_raw = string.replace(telmobil_raw,"(","")
                    telmobil_raw = string.replace(telmobil_raw,")","")
                    telmobil_raw = "%s %s" % (telmobil_raw[0:3],telmobil_raw[3:])
                    telmobil = string.replace(telmobil_raw,countryCodeReplacement,"0")
                    if len(telmobil) > 3:
                        has_phone_mobil = 1
                elif item2.find("HOME") >= 0 and item2.find("VOICE") >= 0:
                    tmp = string.split(item2,":")
                    telhome_raw = string.replace(tmp[1]," ","")
                    telhome_raw = string.replace(telhome_raw,"-","")
                    telhome_raw = string.replace(telhome_raw,"(","")
                    telhome_raw = string.replace(telhome_raw,")","")
                    telhome_raw = "%s %s" % (telhome_raw[0:3],telhome_raw[3:])
                    telhome = string.replace(telhome_raw,countryCodeReplacement,"0")
                    if len(telhome) > 3:
                        has_phone_home = 1
            elif item2.startswith("ORG"):
                tmp = string.split(item2,":")
                org_raw = string.replace(tmp[1],";","")
                org = org_raw.strip()
        if has_phone_home == 1:
            contacts.append([vorname,nachname,org,telhome,catHome])
        if has_phone_mobil == 1:
            contacts.append([vorname,nachname,org,telmobil,catMobile])
        if has_phone_work == 1:
            contacts.append([vorname,nachname,org,telwork,catWork])
    except:
        continue

# Create output file
tmpFilepath = microSipDataPath + '\_Contacts.xml'
f = open(tmpFilepath, 'w')
f.write('<?xml version="1.0"?>\n')
f.write('<contacts>\n')
for item in contacts:
    f.write('<contact number="%s"  name="%s %s (%s, %s)"  presence="0"  directory="0" ></contact>\n'
            % (item[3],item[0],item[1],item[2],item[4]))
f.write('</contacts>\n')
f.close()

# Copy output file
filepath = microSipDataPath + '\Contacts.xml'
shutil.copyfile(tmpFilepath,filepath)
os.remove(tmpFilepath)