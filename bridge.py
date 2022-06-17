# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2022, Roland Rickborn (r_2@gmx.net)
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
# 2022-05-02  Replaced pyCardDAV with vobject
# 2022-06-17  Added reading MicroSIP config to retrieve country code
#
# This script generates Contacts.xml valid for MicroSIP VoIP client v3.10
# ---------------------------------------------------------------------------

import codecs
import configparser
import os
import re

import requests
import vobject
from requests.auth import HTTPBasicAuth

__author__ = 'Roland Rickborn'
__copyright__ = 'Copyright (c) 2022 {}'.format(__author__)
__version__ = '1.0'
__url__ = 'https://github.com/gitRigge/CardDAV2MicroSIP'
__license__ = 'MIT License (MIT)'

microSipDataPath = os.environ['APPDATA']+'\MicroSIP'
bridgeDataPath = os.environ['LOCALAPPDATA']+'\CardDAV2MicroSIP'
bridge_config = configparser.ConfigParser()
bridge_config.read(os.path.join(bridgeDataPath, 'bridge.conf'))
microsip_config = configparser.ConfigParser()
microsip_config.read_file(codecs.open(os.path.join(microSipDataPath, 'microsip.ini'), 'r', 'utf16'))

def get_country_code():
    """Tries to find country code info in MicroSIP config file and returns it."""
    p = re.compile('(\+[0-9]{1,3})')
    for section in microsip_config.sections():
        if microsip_config.has_option(section,'dialPlan'):
            m = p.search(microsip_config.get(section,'dialPlan'))
            if m:
                return m.group(1)
    return '+49'

def get_carddav_data():
    """Retrieves CardDAV data from all accounts specified in the bridge config and returns all content in one string"""
    accounts = {}
    servers = bridge_config.sections()
    counter = 1
    for server in servers:
        accounts[counter] = {}
        _urls = []
        for key in bridge_config[server]:
            if key == 'user':
                accounts[counter]['user'] = bridge_config[server]['user']
            elif key == 'pass':
                accounts[counter]['pass'] = bridge_config[server]['pass']
            elif key.startswith('url'):
                _urls.append(bridge_config[server][key])
        accounts[counter]['url'] = _urls
        counter = counter + 1
    contents = ''
    for account in accounts:
        for abook in accounts[account]['url']:
            try:
                response = requests.get(abook+'/?export', auth = HTTPBasicAuth(accounts[account]['user'], accounts[account]['pass']))
                contents = contents + str(response.content.decode('utf-8'))
            except:
                continue
    return contents

def create_cards_list(file_content):
    """Turns the given string into VCard objects and returns it as a list"""
    _l = str(file_content).replace('\\r\\n','\n').split('END:VCARD')
    _l.pop(-1)
    cards = []
    for i in _l:
        v = vobject.readOne(i+'END:VCARD\n')
        try:
            _o = v.org.value
        except:
            v.add('org').value = ['']
        cards.append(v)
    return cards

def nice_number(phone_number):
    """Strips space, -, ( and ) from the given string, replaces counrty cody with 0 and returns the string"""
    nice_phone_number = phone_number.replace(get_country_code(),'0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
    return nice_phone_number

def export_to_xml(items):
    """Exports the given list into an XML file"""
    f = open(os.path.join(microSipDataPath, 'Contacts.xml'), 'w', encoding='utf8')
    f.write(u'\ufeff')
    f.write('<?xml version="1.0"?>\n')
    f.write('<contacts>\n')
    for item in items:
        try:
            if item.org.value[0] != '':
                _org = '{}, '.format(item.org.value[0])
            else:
                _org = ''
            for tel in item.tel_list:
                if tel.type_param == 'HOME':
                    f.write('<contact number="{}"  name="{} ({}Home)" presence="0" directory="0" ></contact>\n'.format(nice_number(tel.value), item.fn.value, _org))
                elif tel.type_param == 'WORK':
                    f.write('<contact number="{}" name="{} ({}Work)" presence="0" directory="0" ></contact>\n'.format(nice_number(tel.value), item.fn.value, _org))
                elif tel.type_param == 'CELL':
                    f.write('<contact number="{}"  name="{} ({}Mobile)" presence="0" directory="0" ></contact>\n'.format(nice_number(tel.value), item.fn.value, _org))
                else:
                    f.write('<contact number="{}"  name="{} ({}Voice)" presence="0" directory="0" ></contact>\n'.format(nice_number(tel.value), item.fn.value, _org))
        except:
            continue
    f.write('</contacts>\n')
    f.close()

def convert_file_into_xml(fileName):
    """Converts the given file into an XML file"""
    card_list = create_cards_list(fileName)
    export_to_xml(card_list)

vcf = get_carddav_data()
convert_file_into_xml(vcf)
