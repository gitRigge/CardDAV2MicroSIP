# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2021, Roland Rickborn (r_2@gmx.net)
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
# 2021-03-25  Created
#
# Requirements:
# This script requires the CardDAV CLI client pyCardDAV to be installed!
# Get it from here: https://github.com/geier/pycarddav
#
# This script generates Contacts.xml valid for MicroSIP VoIP client v3.10
# ---------------------------------------------------------------------------

import requests
import os
import sys
import configparser

from requests.auth import HTTPBasicAuth
microSipDataPath = os.environ['APPDATA']+"\MicroSIP"
bridgeDataPath = os.environ['LOCALAPPDATA']+"\CardDAV2MicroSIP"
config = configparser.ConfigParser()
config.read(os.path.join(bridgeDataPath, 'bridge.conf'))

def get():
    accounts = {}
    servers = config.sections()
    counter = 1
    for server in servers:
        accounts[counter] = {}
        _urls = []
        for key in config[server]:
            if key == 'user':
                accounts[counter]['user'] = config[server]['user']
            elif key == 'pass':
                accounts[counter]['pass'] = config[server]['pass']
            elif key.startswith('url'):
                _urls.append(config[server][key])
        accounts[counter]['url'] = _urls
        counter = counter + 1
    contents = ''
    for account in accounts:
        for abook in accounts[account]['url']:
            response = requests.get(abook+'/?export', auth = HTTPBasicAuth(accounts[account]['user'], accounts[account]['pass']))
            contents = contents + str(response.content.decode('utf-8'))
    return contents

def create_cards_list(file_content):
    return str(file_content).replace('\\r\\n','\n').split("END:VCARD")

def read_card(item):
    info = {}
    lines = item.replace('\n ','').split('\n')
    tup_lin = [tuple(li.split(":")) for li in lines]
    for d in tup_lin:
        if str(d[0]) == 'FN':
            info["Fullname"] = str(d[1]).strip()
        elif str(d[0]) == 'ORG':
            _org = str(d[1]).replace(';','').strip()
            if _org != '':
                info["Organisation"] = _org
        elif str(d[0]).upper().startswith('TEL'):
            teltypes = d[0].upper()
            if teltypes.find('WORK', 0, len(teltypes)):
                info["WorkTel"] = str(d[1]).replace('+49','0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
            elif teltypes.find('CELL', 0, len(teltypes)):
                info["MobileTel"] = str(d[1]).replace('+49','0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
            elif teltypes.find('HOME', 0, len(teltypes)):
                info["HomeTel"] = str(d[1]).replace('+49','0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
        elif str(d[0]).upper().startswith('ITEMTEL'):
            teltypes = str(d[0]).upper().split('.')
            if 'TEL' in teltypes:
                info["Tel"] = str(d[1]).replace('+49','0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
    return info

def export_to_xml(items):
    f = open(os.path.join(microSipDataPath, 'Contacts.xml'), 'w', encoding='utf8')
    f.write(u'\ufeff')
    f.write('<?xml version="1.0"?>\n')
    f.write('<contacts>\n')
    for item in items:
        if "Organisation" in item:
            if not item["Organisation"] == item["Fullname"]:
                _org = item["Organisation"] + ', '
            else:
                _org = ''
        else:
            _org = ''
        if "WorkTel" in item:
            f.write('<contact number="{}" name="{} ({}Work)" presence="0" directory="0" ></contact>\n'.format(item["WorkTel"], item["Fullname"], _org))
        if "MobileTel" in item:
            f.write('<contact number="{}"  name="{} ({}Mobile)" presence="0" directory="0" ></contact>\n'.format(item["MobileTel"], item["Fullname"], _org))
        if "HomeTel" in item:
            f.write('<contact number="{}"  name="{} ({}Home)" presence="0" directory="0" ></contact>\n'.format(item["HomeTel"], item["Fullname"], _org))
        if "Tel" in item:
            f.write('<contact number="{}"  name="{} ({}Voice)" presence="0" directory="0" ></contact>\n'.format(item["Tel"], item["Fullname"], _org))
    f.write('</contacts>\n')
    f.close()

def convert(fileName):
    card_list = create_cards_list(fileName)
    d_list = [read_card(item) for item in card_list]
    export_to_xml(d_list)

def main_is_frozen():
    return (hasattr(sys, "frozen") or hasattr(sys, "importers"))

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

vcf = get()
convert(vcf)