# CardDAV2MicroSIP
A bridge from cardDAV to the VoIP client MicroSIP

## Introduction
The script bridge.py is able to fetch address data from a CardDAV server. It then generates the file Contacts.xml which is used by the VoIP client MicroSIP as addressbook.
The script setup.py generates a binary of the bridge which can be executed under Windows operating systems.

## Requirements
The scripts require:
* [Python 2.7] (https://www.python.org/download/releases/2.7)
* [pyCardDAV] (https://github.com/geier/pycarddav)
* [MicroSIP 3.10.5] (http://www.microsip.org/downloads)

## Howto
1. Adapt the settings in bridge.py to your needs
2. Adapt the settings of pycard.conf
3. Run makeExe.bat
4. Place the resulting bridge.exe in the startup folder of the Windows start menu
5. Run MicroSIP
