# CardDAV2MicroSIP
A bridge from cardDAV to the VoIP client MicroSIP

## Introduction
The script bridge.py is able to fetch address data from a CardDAV server. It then generates the file Contacts.xml which is used by the VoIP client MicroSIP as addressbook.
The script setup.py generates a binary of the bridge which can be executed under Windows operating systems.

Tested with Python 3.8 and MicroSIP 3.21

## Howto
1. Adapt the settings in bridge.conf to your needs
2. Save bridge.conf in %LOCALAPPDATA%\CardDAV2MicroSIP
3. Run makeExe.bat
4. Place the resulting bridge.exe in the startup folder of the Windows start menu / Run bridge.exe
5. Run MicroSIP