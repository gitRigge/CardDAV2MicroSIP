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
# 2022-05-02  Replaced pyCardDAV with vobject
#
# This script generates Contacts.xml valid for MicroSIP VoIP client v3.10
# ---------------------------------------------------------------------------

import requests
import os
import configparser
import vobject

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
            try:
                response = requests.get(abook+'/?export', auth = HTTPBasicAuth(accounts[account]['user'], accounts[account]['pass']))
                contents = contents + str(response.content.decode('utf-8'))
            except:
                continue
    return contents

def create_cards_list(file_content):
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
    nice_phone_number = phone_number.replace('+49','0').replace(' ' ,'').replace('-' ,'').replace('(' ,'').replace(')' ,'').strip()
    return nice_phone_number

def export_to_xml(items):
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

def convert(fileName):
    card_list = create_cards_list(fileName)
    export_to_xml(card_list)

vcf = get()
convert(vcf)
