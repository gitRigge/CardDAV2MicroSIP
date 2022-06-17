# CardDAV2MicroSIP
A bridge from CardDAV to the VoIP client MicroSIP

## Introduction
The script bridge.py is able to fetch multiple addressbooks from one or more CardDAV servers. It then generates the file Contacts.xml which is used by the VoIP client MicroSIP as addressbook.
The batch file makeExe.bat generates a binary of the bridge which can be executed under Windows operating systems.

Tested with Python 3.8, NextCloud 20.0 and MicroSIP 3.21

## Build
Just run makeExe.bat, wait until it ends and have a look at the release folder.
Or download the latest release from the [GitHub repo release folder](https://github.com/gitRigge/CardDAV2MicroSIP/raw/master/release/bridge.zip)

## Howto
1. Create folder CardDAV2MicroSIP in %LOCALAPPDATA%
2. Store bridge.conf in this folder and adapt it to your needs
3. Run bridge.exe and wait until it ends
4. Run MicroSIP

## Best practice
Put a batch file into your Windows Startup folder like this:

    echo Start CardDAV2MicroSIP
    start bridge.exe
    timeout 10
    echo Start MicroSIP
    start microsip.exe /minimized

## Config
bridge.exe expects its configuration in the file bridge.conf in the folder CardDAV2MicroSIP in %LOCALAPPDATA%.
The config file can specify one or more CardDAV servers with one or more addressbooks.

The file bridge.conf included in the repo specifies two CardDAV servers. The first server holds two addressbooks.
The second server holds only one addressbook.